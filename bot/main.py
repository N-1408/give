# ============================================
# 🤖 Main Entry Point - Telegram Giveaway Bot
# 📁 File: bot/main.py
# 👤 Created by: User with AI
# 📝 Bot entry point that initializes database, registers all
#    handlers and middleware, and starts the bot in either polling
#    mode (local dev) or webhook mode (Render production).
# ============================================
# 📋 CHANGE LOG:
# [2026-03-15 08:06 Tashkent] - Added health check endpoint (/health)
#   and keep-alive self-ping mechanism to prevent Render free tier sleep
# [2026-03-15 10:15 Tashkent] - Fixed dropped messages on Render wake-up
#   by disabling `drop_pending_updates`. App now binds to dynamic `$PORT`.
# [2026-03-15 10:35 Tashkent] - Changed Default ParseMode to HTML 
#   to fix Parse Entities errors throwing TelegramBadRequest
# ============================================

import os
import asyncio
import logging
import sys

import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.config import config
from bot import database as db
from bot.middlewares.i18n import LanguageMiddleware

# 🛤️ Import routers from handlers
from bot.handlers import start, verification, menu, admin

# 📝 Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# ⏰ Keep-alive interval (seconds) — ping self every 10 minutes
KEEP_ALIVE_INTERVAL = 600


# =============================================
# 💓 KEEP-ALIVE SELF-PING (prevents Render sleep)
# =============================================

async def keep_alive_task():
    """💓 Periodically ping own health endpoint to prevent Render free tier sleep"""
    await asyncio.sleep(30)  # ⏳ Wait 30 sec for server to start

    ping_url = f"{config.WEBHOOK_URL}/health"
    logger.info(f"💓 Keep-alive started: pinging {ping_url} every {KEEP_ALIVE_INTERVAL}s")

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ping_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    logger.debug(f"💓 Keep-alive ping: {resp.status}")
        except Exception as e:
            logger.warning(f"⚠️ Keep-alive ping failed: {e}")

        await asyncio.sleep(KEEP_ALIVE_INTERVAL)


async def health_handler(request):
    """🏥 Health check endpoint for Render and keep-alive"""
    return web.json_response({"status": "ok", "bot": "giveaway"})


async def on_startup(bot: Bot):
    """🚀 Actions to perform on bot startup"""
    # 🗄️ Initialize database
    await db.init_db()
    logger.info("✅ Database initialized")

    # 🌐 Set webhook if in webhook mode
    if config.BOT_MODE == "webhook":
        webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=False  # ⚠️ Don't drop updates queued while bot was sleeping!
        )
        logger.info(f"🌐 Webhook set: {webhook_url}")

        # 💓 Start keep-alive background task
        asyncio.create_task(keep_alive_task())
        logger.info("💓 Keep-alive task scheduled")


async def on_shutdown(bot: Bot):
    """🔌 Actions to perform on bot shutdown"""
    # ⚠️ Do NOT delete_webhook() here! Render does rolling updates.
    # If the old container deletes the webhook on shutdown, it breaks the new container.
    await db.close_db()
    logger.info("🔌 Bot shutdown complete")


def create_dispatcher() -> Dispatcher:
    """🏗️ Create and configure the dispatcher"""
    dp = Dispatcher(storage=MemoryStorage())

    # 🌐 Register middleware
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())

    # 🛤️ Register routers (order matters!)
    dp.include_router(start.router)
    dp.include_router(verification.router)
    dp.include_router(menu.router)
    dp.include_router(admin.router)

    # 🚀 Startup/shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return dp


async def run_polling():
    """🔄 Run bot in polling mode (local development)"""
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = create_dispatcher()

    logger.info("🔄 Starting bot in POLLING mode...")
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])


def run_webhook():
    """🌐 Run bot in webhook mode (Render production)"""
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = create_dispatcher()

    # 🌐 Create aiohttp web app
    app = web.Application()

    # 🏥 Register health check endpoint (for keep-alive + monitoring)
    app.router.add_get("/health", health_handler)
    app.router.add_get("/", health_handler)

    # 🔗 Setup webhook handler
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path=config.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    # 🚀 Start web server
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"🌐 Starting bot in WEBHOOK mode on port {port}...")
    web.run_app(app, host="0.0.0.0", port=port)


def main():
    """🏁 Main entry point"""
    if not config.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN is not set! Check your .env file or Render environment.")
        sys.exit(1)

    logger.info(f"🤖 Giveaway Bot starting in {config.BOT_MODE.upper()} mode")

    if config.BOT_MODE == "webhook":
        run_webhook()
    else:
        asyncio.run(run_polling())


if __name__ == "__main__":
    main()

