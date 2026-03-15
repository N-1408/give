# ============================================
# ✅ Verification Handler - Telegram Giveaway Bot
# 📁 File: bot/handlers/verification.py
# 👤 Created by: User with AI
# 📝 Handles channel subscription verification and code issuance.
#    Checks Telegram membership via API, tracks Instagram/YouTube clicks.
#    Issues unique codes and triggers referral rewards upon success.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.enums import ChatMemberStatus
from aiogram.utils.deep_linking import create_start_link
from aiogram.fsm.context import FSMContext

from bot import database as db
from bot.code_generator import generate_unique_code
from bot.texts.messages import get_message
from bot.keyboards.keyboards import (
    get_channels_keyboard,
    get_main_menu_keyboard,
)

logger = logging.getLogger(__name__)

# 🛤️ Router
router = Router()

# ✅ Statuses that mean "subscribed"
SUBSCRIBED_STATUSES = {
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.CREATOR,
}


# =============================================
# ✅ VERIFY CHANNELS CALLBACK
# =============================================

@router.callback_query(F.data == "verify_channels")
async def on_verify_channels(callback: CallbackQuery, bot: Bot, state: FSMContext, lang: str = "uz"):
    """✅ Verify all channel subscriptions"""
    user_id = callback.from_user.id
    await callback.answer()

    # 🔍 Get user from DB
    user = await db.get_user(user_id)
    if not user:
        # 🚫 User not found, restart
        await callback.message.answer("⚠️ Please use /start first.")
        return

    lang = user.get("language", "uz")

    # 🔍 Check if already verified
    if user.get("is_verified"):
        text = await get_message("already_registered", lang)
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=get_main_menu_keyboard(lang))
        return

    # 📢 Get active channels
    channels = await db.get_active_channels()
    missing_channels = []

    for ch in channels:
        ch_type = ch.get("channel_type", "")
        ch_name = ch.get("channel_name", ch_type)

        if ch_type == "telegram":
            # 📢 Telegram: MANDATORY API check
            ch_id = ch.get("channel_id", "")
            if ch_id:
                try:
                    member = await bot.get_chat_member(chat_id=ch_id, user_id=user_id)
                    if member.status in SUBSCRIBED_STATUSES:
                        await db.update_user_field(user_id, "telegram_joined", True)
                        logger.info(f"✅ User {user_id} is subscribed to Telegram: {ch_id}")
                    else:
                        missing_channels.append(f"📢 {ch_name}")
                        logger.info(f"❌ User {user_id} NOT subscribed to Telegram: {ch_id}")
                except Exception as e:
                    logger.error(f"❌ Error checking Telegram membership: {e}")
                    missing_channels.append(f"📢 {ch_name}")

        elif ch_type == "instagram":
            # 📸 Instagram: click tracking (already clicked if button was pressed)
            # Mark as clicked since they interacted with verify
            await db.update_user_field(user_id, "instagram_clicked", True)
            logger.info(f"📸 Instagram marked as clicked for user {user_id}")

        elif ch_type == "youtube":
            # ▶️ YouTube: click tracking
            await db.update_user_field(user_id, "youtube_clicked", True)
            logger.info(f"▶️ YouTube marked as clicked for user {user_id}")

    # ❌ If missing channels, show error
    if missing_channels:
        missing_text = "\n".join(missing_channels)
        text = await get_message("not_verified", lang, missing_channels=missing_text)
        channels = await db.get_active_channels()
        await callback.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=get_channels_keyboard(channels, lang)
        )
        return

    # ✅ All verified! Generate code and referral link
    await db.update_user_field(user_id, "is_verified", True)

    # 🎟️ Generate unique code
    code = await generate_unique_code()
    await db.save_code(
        user_id=user_id,
        code=code,
        code_type="subscription"
    )

    # 🔗 Generate referral link
    referral_link = await create_start_link(bot, f"ref_{user_id}")

    # 🎉 Send success message with code
    success_text = await get_message("verification_success", lang)
    await callback.message.edit_text(success_text, parse_mode="Markdown")

    code_text = await get_message("code_message", lang, code=code, referral_link=referral_link)
    await callback.message.answer(
        code_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang)
    )

    logger.info(f"🎟️ Code issued to user {user_id}: {code}")

    # 🔗 Process referral reward
    referrer_id = user.get("referrer_id")
    if referrer_id:
        await _process_referral_reward(bot, referrer_id, user_id, callback.from_user)

    # 🧹 Clear FSM state
    await state.clear()


# =============================================
# 🔗 REFERRAL REWARD PROCESSING
# =============================================

async def _process_referral_reward(bot: Bot, referrer_id: int, new_user_id: int, new_user):
    """🔗 Award bonus code to referrer and notify them"""
    try:
        # 🔍 Check if referrer exists and is verified
        referrer = await db.get_user(referrer_id)
        if not referrer or not referrer.get("is_verified"):
            logger.warning(f"⚠️ Referrer {referrer_id} not found or not verified")
            return

        referrer_lang = referrer.get("language", "uz")

        # 🎟️ Generate bonus code for referrer
        bonus_code = await generate_unique_code()
        await db.save_code(
            user_id=referrer_id,
            code=bonus_code,
            code_type="referral",
            referred_user_id=new_user_id
        )

        # 📊 Get total codes count for referrer
        total_codes = await db.get_user_code_count(referrer_id)

        # 👤 Build user display name
        name = new_user.first_name or ""
        if new_user.last_name:
            name += f" {new_user.last_name}"
        if not name.strip():
            name = f"User {new_user_id}"

        # 🔔 Notify referrer
        notification = await get_message(
            "referral_notification", referrer_lang,
            name=name, code=bonus_code, total=total_codes
        )
        await bot.send_message(referrer_id, notification, parse_mode="Markdown")

        logger.info(f"🎟️ Referral bonus: {bonus_code} → {referrer_id} (from {new_user_id})")

    except Exception as e:
        logger.error(f"❌ Error processing referral reward: {e}")
