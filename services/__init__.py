"""
Services module for Cereal Bot
Provides external API integration layers
"""

from .ai_service import AIService, ai_service

__all__ = [
    'AIService',
    'ai_service',
]