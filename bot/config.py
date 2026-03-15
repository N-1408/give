# ============================================
# ⚙️ Configuration Module - Telegram Giveaway Bot
# 📁 File: bot/config.py
# 👤 Created by: User with AI
# 📝 Loads all environment variables from .env file or
#    Render environment. Provides centralized access to
#    bot configuration, database credentials, and settings.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

import os
from dotenv import load_dotenv

# 🔄 Load .env file (only works locally, Render uses its own env)
load_dotenv()


class Config:
    """⚙️ Central configuration class for the giveaway bot"""

    # 🤖 Telegram Bot
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    # 🗄️ Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL", "")

    # 🌐 Webhook (production)
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")

    # 🔐 Admin password for /shep command
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "qizildevzira")

    # 🚀 Bot mode: 'polling' for dev, 'webhook' for production
    BOT_MODE: str = os.getenv("BOT_MODE", "polling")

    # 📢 Default channel info (fallback if DB is empty)
    DEFAULT_CHANNELS = {
        "telegram": {
            "id": "@aliypubgm",
            "url": "https://t.me/aliypubgm",
            "name": "Aliy PUBGM"
        },
        "instagram": {
            "url": "https://www.instagram.com/aliypubgm_",
            "name": "aliypubgm_"
        },
        "youtube": {
            "url": "https://www.youtube.com/@aliypubgm",
            "name": "Aliy PUBGM"
        }
    }

    # 🌐 Supported languages
    LANGUAGES = ["uz", "ru", "en"]

    # 📊 Broadcast rate limit (messages per second)
    BROADCAST_RATE = 25


# 🏗️ Create singleton config instance
config = Config()
