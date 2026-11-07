"""
Shared Reddit meme fetching for Cereal Bot

Used by both /meme (cogs/fun.py) and the auto-meme poster (cogs/automeme.py)
so there's a single source of truth for subreddit selection, NSFW filtering
and embed construction.
"""

import random

import aiohttp
import discord

MEME_SUBREDDITS = ['memes', 'dankmemes', 'me_irl', 'whenthe', 'HistoryMemes']
MEME_API_TIMEOUT = aiohttp.ClientTimeout(total=10)


async def fetch_random_meme(session, subreddits=None, max_attempts=3):
    """
    Fetch a random SFW meme via meme-api (no auth required).

    Args:
        session: aiohttp.ClientSession to use
        subreddits: Subreddits to choose from (defaults to MEME_SUBREDDITS)
        max_attempts: Number of API calls to try before giving up

    Returns:
        Raw meme-api dict (title, url, postLink, ups, subreddit, ...) or
        None when every attempt failed.
    """
    subs = list(subreddits) if subreddits else MEME_SUBREDDITS

    for _ in range(max_attempts):
        subreddit = random.choice(subs)
        try:
            async with session.get(
                f'https://meme-api.com/gimme/{subreddit}',
                timeout=MEME_API_TIMEOUT,
            ) as resp:
                if resp.status != 200:
                    continue

                data = await resp.json()

                # Skip NSFW posts and entries without an image URL
                if data.get('nsfw'):
                    continue
                if not data.get('url'):
                    continue

                return data

        except Exception:
            continue

    return None


def build_meme_embed(data, footer_prefix=None):
    """
    Build the standard meme embed from a meme-api payload.

    Args:
        data: dict from meme-api (title, url, postLink, ups, subreddit)
        footer_prefix: optional leading footer text (e.g. 'Auto-meme')
    """
    footer_bits = []
    if footer_prefix:
        footer_bits.append(footer_prefix)
    footer_bits.append(f"{data.get('ups', 0)} upvotes")
    subreddit = data.get('subreddit')
    if subreddit:
        footer_bits.append(f"r/{subreddit}")

    embed = discord.Embed(
        title=(data.get('title') or 'Meme')[:256],  # Discord title limit
        color=discord.Color.random(),
        url=data.get('postLink')
    )
    embed.set_image(url=data.get('url'))
    embed.set_footer(text=' | '.join(footer_bits))
    return embed
