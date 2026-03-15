# ============================================
# 🚀 Start Handler - Telegram Giveaway Bot
# 📁 File: bot/handlers/start.py
# 👤 Created by: User with AI
# 📝 Handles the /start command flow: welcome message, language
#    selection, contact sharing, and deep link referral tracking.
#    This is the entry point for all new users joining the bot.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot import database as db
from bot.texts.messages import get_message
from bot.keyboards.keyboards import (
    get_language_keyboard,
    get_contact_keyboard,
    get_channels_keyboard,
    get_main_menu_keyboard,
)

logger = logging.getLogger(__name__)

# 🔄 FSM States for registration flow
class RegistrationStates(StatesGroup):
    waiting_language = State()      # 🌐 Waiting for language selection
    waiting_contact = State()       # 📱 Waiting for phone contact
    waiting_verification = State()  # ✅ Waiting for channel verification

# 🛤️ Router
router = Router()


# =============================================
# 🚀 /START COMMAND
# =============================================

@router.message(CommandStart(deep_link=True))
async def cmd_start_with_referral(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    """🚀 Handle /start with referral deep link (e.g. /start ref_123456)"""
    # 🔍 Decode referral payload
    referrer_id = None
    if command.args:
        try:
            payload = command.args
            if payload.startswith("ref_"):
                referrer_id = int(payload.replace("ref_", ""))
                logger.info(f"🔗 Referral detected: {referrer_id} → {message.from_user.id}")
        except (ValueError, Exception) as e:
            logger.warning(f"⚠️ Invalid referral payload: {command.args} - {e}")

    # 💾 Save referrer_id in FSM state
    await state.update_data(referrer_id=referrer_id)

    # 🔍 Check if user already exists and has a phone
    existing_user = await db.get_user(message.from_user.id)
    if existing_user and existing_user.get("phone"):
        lang = existing_user.get("language", "uz")
        text = await get_message("already_registered", lang)
        await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu_keyboard(lang))
        await state.clear()
        return

    # 🌐 Show language selection
    text = await get_message("choose_language", "uz")
    await message.answer(text, parse_mode="HTML", reply_markup=get_language_keyboard())
    await state.set_state(RegistrationStates.waiting_language)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    """🚀 Handle /start without referral"""
    # 🔍 Check if user already exists and has a phone
    existing_user = await db.get_user(message.from_user.id)
    if existing_user and existing_user.get("phone"):
        lang = existing_user.get("language", "uz")
        text = await get_message("already_registered", lang)
        await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu_keyboard(lang))
        await state.clear()
        return

    # 🌐 Show language selection
    text = await get_message("choose_language", "uz")
    await message.answer(text, parse_mode="HTML", reply_markup=get_language_keyboard())
    await state.set_state(RegistrationStates.waiting_language)


# =============================================
# 🌐 LANGUAGE SELECTION CALLBACK
# =============================================

@router.callback_query(F.data.startswith("lang_"))
async def on_language_selected(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """🌐 Handle language selection"""
    lang = callback.data.replace("lang_", "")

    # 💾 Save language in FSM state
    await state.update_data(language=lang)

    # ✅ Answer callback
    await callback.answer()

    # 🔍 Check if user already exists and has a phone
    user = await db.get_user(callback.from_user.id)
    if user and user.get("phone"):
        # 🔄 Update existing user's language
        await db.update_user_field(user['telegram_id'], "language", lang)
        
        # 📝 Send success message and new menu
        from bot.keyboards.keyboards import get_main_menu_keyboard
        texts = {"uz": "✅ Til o'zgartirildi", "ru": "✅ Язык изменен", "en": "✅ Language changed"}
        await callback.message.delete() # Remove inline keyboard
        await callback.message.answer(
            texts.get(lang, texts["uz"]),
            parse_mode="HTML",
            reply_markup=get_main_menu_keyboard(lang)
        )
        return

    # 📱 Ask for contact (New user)
    text = await get_message("ask_contact", lang)
    await callback.message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_contact_keyboard(lang)
    )
    await state.set_state(RegistrationStates.waiting_contact)


# =============================================
# 📱 CONTACT SHARING HANDLER
# =============================================

@router.message(RegistrationStates.waiting_contact, F.contact)
async def on_contact_received(message: Message, state: FSMContext, bot: Bot):
    """📱 Handle received phone contact"""
    contact = message.contact
    user = message.from_user
    state_data = await state.get_data()

    lang = state_data.get("language", "uz")
    referrer_id = state_data.get("referrer_id")

    # 🔒 Don't allow self-referral
    if referrer_id and referrer_id == user.id:
        referrer_id = None

    # 💾 Save user to database
    await db.save_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=contact.phone_number,
        language=lang,
        referrer_id=referrer_id
    )

    logger.info(f"💾 User saved: {user.id} ({user.first_name}) | Phone: {contact.phone_number}")

    # 📢 Show channel subscription links
    channels = await db.get_active_channels()
    text = await get_message("channels_intro", lang)
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_channels_keyboard(channels, lang)
    )
    await state.set_state(RegistrationStates.waiting_verification)
