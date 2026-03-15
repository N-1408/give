# ============================================
# ⌨️ Keyboards Module - Telegram Giveaway Bot
# 📁 File: bot/keyboards/keyboards.py
# 👤 Created by: User with AI
# 📝 All keyboard markup definitions for the bot.
#    Includes reply keyboards (contact, menu) and
#    inline keyboards (language, channels, admin panel).
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from typing import List


# =============================================
# 🌐 LANGUAGE SELECTION
# =============================================

def get_language_keyboard() -> InlineKeyboardMarkup:
    """🌐 Language selection inline keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        ]
    ])


# =============================================
# 📱 CONTACT SHARING
# =============================================

def get_contact_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """📱 Contact sharing reply keyboard"""
    texts = {
        "uz": "📱 Telefon raqamni yuborish",
        "ru": "📱 Отправить номер телефона",
        "en": "📱 Share phone number"
    }
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.get(language, texts["uz"]), request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# =============================================
# 📢 CHANNEL SUBSCRIPTION
# =============================================

def get_channels_keyboard(channels: List[dict], language: str = "uz") -> InlineKeyboardMarkup:
    """📢 Channel subscription inline keyboard with verify button"""
    buttons = []

    # 🔗 Channel buttons
    for ch in channels:
        ch_type = ch.get("channel_type", "")
        ch_name = ch.get("channel_name", ch_type.title())
        ch_url = ch.get("channel_url", "")

        # 📋 Emoji per channel type
        emoji_map = {
            "telegram": "📢",
            "instagram": "📸",
            "youtube": "▶️"
        }
        emoji = emoji_map.get(ch_type, "🔗")

        # 🌐 Subscribe text per language
        sub_text = {
            "uz": "Obuna bo'lish",
            "ru": "Подписаться",
            "en": "Subscribe"
        }

        buttons.append([
            InlineKeyboardButton(
                text=f"{emoji} {ch_name} — {sub_text.get(language, sub_text['uz'])} ➜",
                url=ch_url
            )
        ])

    # ✅ Verify button
    verify_text = {
        "uz": "✅ Tekshirish",
        "ru": "✅ Проверить",
        "en": "✅ Verify"
    }
    buttons.append([
        InlineKeyboardButton(
            text=verify_text.get(language, verify_text["uz"]),
            callback_data="verify_channels"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# =============================================
# 📋 MAIN MENU
# =============================================

def get_main_menu_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """📋 Main menu reply keyboard"""
    menus = {
        "uz": [
            ["🎟️ Mening imkoniyatlarim", "🔗 Referal linkim"],
            ["🏆 Top referallar", "📋 Qoidalar"],
            ["🎁 Sovrinlar", "📩 Adminga murojaat"]
        ],
        "ru": [
            ["🎟️ Мои шансы", "🔗 Моя реферальная ссылка"],
            ["🏆 Топ рефералы", "📋 Правила"],
            ["🎁 Призы", "📩 Связаться с админом"]
        ],
        "en": [
            ["🎟️ My chances", "🔗 My referral link"],
            ["🏆 Top referrers", "📋 Rules"],
            ["🎁 Prizes", "📩 Contact admin"]
        ]
    }

    menu = menus.get(language, menus["uz"])
    keyboard = [[KeyboardButton(text=btn) for btn in row] for row in menu]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# =============================================
# 👑 ADMIN PANEL
# =============================================

def get_admin_keyboard(language: str = "uz") -> InlineKeyboardMarkup:
    """👑 Admin panel inline keyboard"""
    buttons = {
        "uz": [
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📝 Textlarni o'zgartirish", callback_data="admin_edit_texts")],
            [InlineKeyboardButton(text="📥 Excel yuklab olish", callback_data="admin_export")],
            [InlineKeyboardButton(text="📢 Xabar yuborish (Broadcast)", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔄 Kanal sozlamalari", callback_data="admin_channels")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_close")],
        ],
        "ru": [
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📝 Редактировать тексты", callback_data="admin_edit_texts")],
            [InlineKeyboardButton(text="📥 Скачать Excel", callback_data="admin_export")],
            [InlineKeyboardButton(text="📢 Рассылка (Broadcast)", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔄 Настройки каналов", callback_data="admin_channels")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_close")],
        ],
        "en": [
            [InlineKeyboardButton(text="📊 Statistics", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📝 Edit texts", callback_data="admin_edit_texts")],
            [InlineKeyboardButton(text="📥 Download Excel", callback_data="admin_export")],
            [InlineKeyboardButton(text="📢 Broadcast message", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔄 Channel settings", callback_data="admin_channels")],
            [InlineKeyboardButton(text="🔙 Back", callback_data="admin_close")],
        ]
    }

    return InlineKeyboardMarkup(
        inline_keyboard=buttons.get(language, buttons["uz"])
    )


def get_text_keys_keyboard() -> InlineKeyboardMarkup:
    """📝 Text keys selection for admin editing"""
    keys = [
        ("welcome", "🏠 Welcome"),
        ("ask_contact", "📱 Ask Contact"),
        ("channels_intro", "📢 Channels Intro"),
        ("verification_success", "✅ Verification Success"),
        ("code_message", "🎟️ Code Message"),
        ("referral_info", "🔗 Referral Info"),
        ("referral_notification", "🔔 Referral Notification"),
        ("my_chances", "🎟️ My Chances"),
        ("rules", "📋 Rules"),
        ("prizes", "🎁 Prizes"),
        ("contact_admin", "📩 Contact Admin"),
        ("already_registered", "⚠️ Already Registered"),
        ("not_verified", "❌ Not Verified"),
    ]
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"edit_text_{key}")]
        for key, label in keys
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_language_select_keyboard(text_key: str) -> InlineKeyboardMarkup:
    """🌐 Language selection for text editing"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data=f"textlang_{text_key}_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data=f"textlang_{text_key}_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data=f"textlang_{text_key}_en"),
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_edit_texts")]
    ])


def get_confirm_broadcast_keyboard(language: str = "uz") -> InlineKeyboardMarkup:
    """📢 Broadcast confirmation keyboard"""
    texts = {
        "uz": ("✅ Yuborish", "❌ Bekor qilish"),
        "ru": ("✅ Отправить", "❌ Отменить"),
        "en": ("✅ Send", "❌ Cancel"),
    }
    confirm, cancel = texts.get(language, texts["uz"])
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm, callback_data="broadcast_confirm"),
            InlineKeyboardButton(text=cancel, callback_data="broadcast_cancel"),
        ]
    ])
