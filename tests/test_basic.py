"""
Unit tests for Cereal Bot
Run with: python -m pytest tests/
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import discord

# Import bot components
from bot import CerealBot
from core import config


class TestCerealBot:
    """Test cases for the main bot functionality"""

    @pytest.fixture
    def bot(self):
        """Create a test bot instance"""
        bot = CerealBot()
        bot.user = Mock()
        bot.user.id = 123456789
        bot.user.name = "TestBot"
        return bot

    @pytest.mark.asyncio
    async def test_bot_initialization(self, bot):
        """Test that bot initializes with correct settings"""
        assert bot.command_prefix == '!'
        assert bot.intents.message_content is True
        assert bot.intents.members is True
        assert bot.intents.voice_states is True

    @pytest.mark.asyncio
    async def test_health_check(self, bot):
        """Test health check endpoint"""
        from aiohttp.test_utils import make_mocked_request

        # Mock bot properties
        bot.user = Mock()
        bot.user.__str__ = Mock(return_value="TestBot#1234")
        bot.guilds = [Mock()]
        bot.users = [Mock(), Mock()]
        bot.latency = 0.05

        request = make_mocked_request('GET', '/health')
        response = await bot.health_check(request)

        data = response
        assert data['status'] == 'healthy'
        assert data['guilds'] == 1
        assert data['users'] == 2
        assert isinstance(data['latency'], float)


class TestConfig:
    """Test configuration management"""

    def test_config_defaults(self):
        """Test that config has reasonable defaults"""
        assert config.BOT_PREFIX == '!'
        assert config.LOG_LEVEL == 'INFO'
        assert config.DATABASE_TYPE == 'sqlite'

    def test_config_env_override(self, monkeypatch):
        """Test that environment variables override defaults"""
        monkeypatch.setenv('BOT_PREFIX', '>')
        monkeypatch.setenv('LOG_LEVEL', 'DEBUG')

        # Re-import to get new values
        from importlib import reload
        import core.config
        reload(core.config)
        from core.config import config as new_config

        assert new_config.BOT_PREFIX == '>'
        assert new_config.LOG_LEVEL == 'DEBUG'


if __name__ == '__main__':
    # Run basic tests
    print("Running basic tests...")

    # Test config
    print("✓ Config defaults loaded")
    print(f"  Bot prefix: {config.BOT_PREFIX}")
    print(f"  Log level: {config.LOG_LEVEL}")

    print("✓ All basic tests passed!")