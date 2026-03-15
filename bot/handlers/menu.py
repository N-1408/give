# ============================================
# 📋 Menu Handler - Telegram Giveaway Bot
# 📁 File: bot/handlers/menu.py
# 👤 Created by: User with AI
# 📝 Handles all main menu interactions: my chances, referral
#    link, top referrers leaderboard, rules, prizes, and
#    contact admin. Responds to reply keyboard button presses.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from bot import database as db
from bot.texts.messages import get_message, get_text_with_image

logger = logging.getLogger(__name__)

# 🛤️ Router
router = Router()


# =============================================
# 🎟️ MY CHANCES
# =============================================

@router.message(F.text.in_({
    "🎟️ Mening imkoniyatlarim", "🎟️ Мои шансы", "🎟️ My chances"
}))
async def on_my_chances(message: Message, bot: Bot, lang: str = "uz"):
    """🎟️ Show user's codes and chances count"""
    user_id = message.from_user.id

    # 📋 Get user codes
    codes = await db.get_user_codes(user_id)
    total = len(codes)
    referral_count = sum(1 for c in codes if c["code_type"] == "referral")

    # 📝 Format codes list
    if codes:
        codes_list = "\n".join([
            f"{'🎫' if c['code_type'] == 'subscription' else '🔗'} `{c['code']}` ({c['code_type']})"
            for c in codes
        ])
    else:
        codes_list = "—"

    text = await get_message(
        "my_chances", lang,
        total=total, referral_count=referral_count, codes_list=codes_list
    )
    await message.answer(text, parse_mode="Markdown")


# =============================================
# 🔗 MY REFERRAL LINK
# =============================================

@router.message(F.text.in_({
    "🔗 Referal linkim", "🔗 Моя реферальная ссылка", "🔗 My referral link"
}))
async def on_referral_link(message: Message, bot: Bot, lang: str = "uz"):
    """🔗 Show user's referral link"""
    user_id = message.from_user.id
    referral_link = await create_start_link(bot, f"ref_{user_id}")

    text = await get_message("referral_info", lang, referral_link=referral_link)
    await message.answer(text, parse_mode="Markdown")


# =============================================
# 🏆 TOP REFERRERS
# =============================================

@router.message(F.text.in_({
    "🏆 Top referallar", "🏆 Топ рефералы", "🏆 Top referrers"
}))
async def on_top_referrers(message: Message, lang: str = "uz"):
    """🏆 Show top 10 referrers leaderboard"""
    top = await db.get_top_referrers(limit=10)

    if top:
        leaderboard_lines = []
        for i, user in enumerate(top, 1):
            # 🏅 Medal emoji for top 3
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")

            # 👤 Display name
            name = user.get("first_name", "")
            if user.get("last_name"):
                name += f" {user['last_name']}"
            if not name.strip():
                name = f"@{user.get('username', 'Unknown')}"

            count = user.get("referral_count", 0)
            leaderboard_lines.append(f"{medal} {name} — *{count}* referral")

        leaderboard = "\n".join(leaderboard_lines)
    else:
        leaderboard_empty = {
            "uz": "Hozircha hech kim referral qilmagan 🤷",
            "ru": "Пока никто не пригласил друзей 🤷",
            "en": "No referrals yet 🤷"
        }
        leaderboard = leaderboard_empty.get(lang, leaderboard_empty["uz"])

    text = await get_message("top_referrers", lang, leaderboard=leaderboard)
    await message.answer(text, parse_mode="Markdown")


# =============================================
# 📋 RULES
# =============================================

@router.message(F.text.in_({
    "📋 Qoidalar", "📋 Правила", "📋 Rules"
}))
async def on_rules(message: Message, lang: str = "uz"):
    """📋 Show giveaway rules"""
    content, image_id = await get_text_with_image("rules", lang)

    if image_id:
        await message.answer_photo(photo=image_id, caption=content, parse_mode="Markdown")
    else:
        await message.answer(content, parse_mode="Markdown")


# =============================================
# 🎁 PRIZES
# =============================================

@router.message(F.text.in_({
    "🎁 Sovrinlar", "🎁 Призы", "🎁 Prizes"
}))
async def on_prizes(message: Message, lang: str = "uz"):
    """🎁 Show prizes info"""
    content, image_id = await get_text_with_image("prizes", lang)

    if image_id:
        await message.answer_photo(photo=image_id, caption=content, parse_mode="Markdown")
    else:
        await message.answer(content, parse_mode="Markdown")


# =============================================
# 📩 CONTACT ADMIN
# =============================================

@router.message(F.text.in_({
    "📩 Adminga murojaat", "📩 Связаться с админом", "📩 Contact admin"
}))
async def on_contact_admin(message: Message, lang: str = "uz"):
    """📩 Show admin contact info"""
    text = await get_message("contact_admin", lang)
    await message.answer(text, parse_mode="Markdown")
