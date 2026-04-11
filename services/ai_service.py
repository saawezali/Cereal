"""
AI Service Layer for Cereal Bot
Handles all Groq API interactions with retry logic, rate limiting, and error handling.
NEVER call the AI API directly from command handlers — use this service instead.
"""

import asyncio
import time
from typing import List, Dict, Optional

import groq
from groq import Groq, APIStatusError, RateLimitError

from core.config import config
from core.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# System prompts — kept short to minimise token usage
# ---------------------------------------------------------------------------

CHAT_SYSTEM_PROMPT = (
    "You are Cereal, a helpful and concise Discord bot with a slightly witty personality. "
    "Keep answers short (under 400 words), use markdown formatting, and stay friendly. "
    "If you don't know something, say so honestly."
)

SUMMARY_SYSTEM_PROMPT = (
    "You are a summarisation assistant. Produce concise bullet-point summaries. "
    "Highlight: key topics, decisions, and action items. "
    "Use markdown formatting. Keep the summary under 500 words."
)


class AIService:
    """
    Thin async wrapper around the Groq chat-completions API.

    Features:
    * Exponential-backoff retry on HTTP 429 (rate-limit) and transient 5xx errors
    * Per-request token budgeting
    * Clean error messages suitable for Discord
    """

    # Groq model identifiers
    CHAT_MODEL: str = "llama-3.3-70b-versatile"
    SUMMARY_MODEL: str = "llama-3.3-70b-versatile"

    # Retry configuration
    MAX_RETRIES: int = 3
    BASE_DELAY: float = 1.0          # seconds — doubled on each retry
    MAX_DELAY: float = 10.0          # cap for exponential back-off

    # Token budgets
    CHAT_MAX_TOKENS: int = 512
    SUMMARY_MAX_TOKENS: int = 700

    # Temperature
    CHAT_TEMPERATURE: float = 0.7
    SUMMARY_TEMPERATURE: float = 0.3   # lower = more factual

    def __init__(self):
        self._client: Optional[Groq] = None
        self._initialized: bool = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """
        Initialise the Groq client from the GROQ_API_KEY env var.
        Called once during bot startup.
        """
        api_key = config.GROQ_API_KEY
        if not api_key:
            logger.warning("GROQ_API_KEY not set — AI commands will be unavailable")
            return

        self._client = Groq(api_key=api_key)
        self._initialized = True
        logger.info("✓ AI service initialised (Groq)")

    @property
    def is_ready(self) -> bool:
        """Whether the service is configured and ready to accept requests."""
        return self._initialized and self._client is not None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def ask(
        self,
        user_message: str,
        context_messages: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Generate a smart chat response.

        Args:
            user_message:   The user's question / prompt.
            context_messages: Optional list of recent messages for conversational
                              context, each dict with 'role' and 'content' keys.

        Returns:
            The assistant's reply text, or a user-friendly error string.
        """
        if not self.is_ready:
            return "⚠️ AI features are currently unavailable (API key not configured)."

        messages: List[Dict[str, str]] = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]

        # Append conversation context (kept short to save tokens)
        if context_messages:
            messages.extend(context_messages[-10:])  # cap at last 10 messages

        messages.append({"role": "user", "content": user_message})

        return await self._call(
            messages=messages,
            model=self.CHAT_MODEL,
            max_tokens=self.CHAT_MAX_TOKENS,
            temperature=self.CHAT_TEMPERATURE,
            feature="ask",
        )

    async def summarize(
        self,
        messages_text: str,
        channel_name: str = "channel",
    ) -> str:
        """
        Generate a concise bullet-point summary of a block of messages.

        Args:
            messages_text:  Pre-formatted string of messages to summarise.
            channel_name:  Name of the source channel (used in prompt only).

        Returns:
            The summary text, or a user-friendly error string.
        """
        if not self.is_ready:
            return "⚠️ AI features are currently unavailable (API key not configured)."

        # Chunk if the input is very large (rough heuristic: ~4 chars per token)
        chunks = self._chunk_text(messages_text, max_chars=12000)
        if not chunks:
            return "⚠️ No messages to summarise."

        # If there's only one chunk, summarise directly
        if len(chunks) == 1:
            return await self._summarise_single(chunks[0], channel_name)

        # Multiple chunks: summarise each, then merge
        partial_summaries: List[str] = []
        for idx, chunk in enumerate(chunks, 1):
            summary = await self._summarise_single(
                chunk, channel_name, part_label=f" (part {idx}/{len(chunks)})"
            )
            if summary.startswith("⚠️") or summary.startswith("❌"):
                return summary  # propagate error
            partial_summaries.append(summary)

        merged = "\n\n".join(partial_summaries)
        return await self._summarise_single(
            merged, channel_name, part_label=" (merged summary)"
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _summarise_single(
        self,
        text: str,
        channel_name: str,
        part_label: str = "",
    ) -> str:
        """Summarise a single chunk of messages."""
        user_content = (
            f"Summarise the following messages from #{channel_name}{part_label}:\n\n{text}"
        )

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]

        return await self._call(
            messages=messages,
            model=self.SUMMARY_MODEL,
            max_tokens=self.SUMMARY_MAX_TOKENS,
            temperature=self.SUMMARY_TEMPERATURE,
            feature="summarize",
        )

    async def _call(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: int,
        temperature: float,
        feature: str,
    ) -> str:
        """
        Low-level Groq API call with exponential-backoff retry on rate limits.

        Returns:
            The assistant's reply content, or a user-friendly error string.
        """
        last_exception: Optional[Exception] = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                # Groq SDK is synchronous — run in executor to avoid blocking
                response = await asyncio.to_thread(
                    self._client.chat.completions.create,
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

                content = response.choices[0].message.content
                if content:
                    logger.info(
                        f"AI call succeeded (feature={feature}, attempt={attempt}, "
                        f"model={model}, tokens={getattr(response, 'usage', 'n/a')})"
                    )
                    return content.strip()

                # Empty response — treat as error
                logger.warning(f"AI returned empty content (feature={feature})")
                return "⚠️ AI returned an empty response. Please try again."

            except RateLimitError as exc:
                last_exception = exc
                delay = min(self.BASE_DELAY * (2 ** (attempt - 1)), self.MAX_DELAY)
                logger.warning(
                    f"Rate limited (feature={feature}, attempt={attempt}/{self.MAX_RETRIES}, "
                    f"retry_in={delay:.1f}s): {exc}"
                )
                await asyncio.sleep(delay)

            except APIStatusError as exc:
                last_exception = exc
                if exc.status_code == 429:
                    # Some 429s come as APIStatusError instead of RateLimitError
                    delay = min(self.BASE_DELAY * (2 ** (attempt - 1)), self.MAX_DELAY)
                    logger.warning(
                        f"HTTP 429 via APIStatusError (feature={feature}, attempt={attempt}, "
                        f"retry_in={delay:.1f}s)"
                    )
                    await asyncio.sleep(delay)
                elif 500 <= exc.status_code < 600:
                    # Transient server error — retry
                    delay = min(self.BASE_DELAY * (2 ** (attempt - 1)), self.MAX_DELAY)
                    logger.warning(
                        f"Server error {exc.status_code} (feature={feature}, attempt={attempt}, "
                        f"retry_in={delay:.1f}s)"
                    )
                    await asyncio.sleep(delay)
                else:
                    # Non-retryable HTTP error
                    logger.error(f"Groq API error (feature={feature}): {exc}")
                    return "❌ AI service error. Please try again later."

            except Exception as exc:
                last_exception = exc
                logger.error(f"Unexpected AI error (feature={feature}): {exc}", exc_info=True)
                return "❌ Something went wrong with the AI service. Please try again later."

        # All retries exhausted
        logger.error(
            f"All {self.MAX_RETRIES} retries exhausted (feature={feature}): {last_exception}"
        )
        return "❌ AI service is currently busy. Please try again in a moment."

    @staticmethod
    def _chunk_text(text: str, max_chars: int = 12000) -> List[str]:
        """
        Split text into chunks that fit within the token budget.

        Uses a simple character-count heuristic (~4 chars per token).
        Splits on double-newlines to keep message boundaries intact.
        """
        if len(text) <= max_chars:
            return [text]

        chunks: List[str] = []
        current: List[str] = []
        current_len = 0

        for line in text.split("\n"):
            line_len = len(line) + 1  # +1 for the newline
            if current_len + line_len > max_chars and current:
                chunks.append("\n".join(current))
                current = []
                current_len = 0
            current.append(line)
            current_len += line_len

        if current:
            chunks.append("\n".join(current))

        return chunks


# ---------------------------------------------------------------------------
# Module-level singleton — import and use across cogs
# ---------------------------------------------------------------------------

ai_service = AIService()