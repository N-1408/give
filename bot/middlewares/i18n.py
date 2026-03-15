# ============================================
# 🌐 i18n Middleware - Telegram Giveaway Bot
# 📁 File: bot/middlewares/i18n.py
# 👤 Created by: User with AI
# 📝 Middleware that loads the user's language preference
#    from the database and injects it into handler data.
#    Falls back to 'uz' if user is not found or has no preference.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery
from bot import database as db

logger = logging.getLogger(__name__)


class LanguageMiddleware(BaseMiddleware):
    """
    🌐 Language middleware

    Loads user language from DB and passes it to handlers via data["lang"]
    """

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        # 🔍 Extract telegram_id from event
        telegram_id = None

        if isinstance(event, Message) and event.from_user:
            telegram_id = event.from_user.id
        elif isinstance(event, CallbackQuery) and event.from_user:
            telegram_id = event.from_user.id

        # 🌐 Get language from DB (default: uz)
        lang = "uz"
        if telegram_id:
            try:
                user = await db.get_user(telegram_id)
                if user and user.get("language"):
                    lang = user["language"]
            except Exception as e:
                logger.warning(f"⚠️ Failed to get user language: {e}")

        # 💉 Inject language into handler data
        data["lang"] = lang

        return await handler(event, data)
