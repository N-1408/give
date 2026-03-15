# ============================================
# ⌨️ Keyboards Module - Telegram Giveaway Bot
# 📁 File: bot/keyboards/keyboards.py
# 👤 Created by: User with AI
# 📝 All keyboard markup definitions for the bot.
#    Includes reply keyboards (contact, menu) and
#    inline keyboards (language, channels, admin panel).
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================
# 📋 CHANGE LOG:
# [2026-03-15 09:18 Tashkent] - Removed Top referallar & Adminga murojaat
#   from menu. Added admin reply keyboard. Simplified main menu to 2 rows.
# [2026-03-15 09:40 Tashkent] - Updated admin menu: renamed Broadcast
#   to Barchaga xabar yuborish, swapped positions, removed user menus.
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

        buttons.append([
            InlineKeyboardButton(
                text=f"{emoji} {ch_name}",
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
# 📋 MAIN MENU (for regular users)
# =============================================

def get_main_menu_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """📋 Main menu reply keyboard (users only)"""
    menus = {
        "uz": [
            ["🎟️ Mening imkoniyatlarim", "🔗 Referal linkim"],
            ["📋 Qoidalar", "🎁 Sovrinlar"],
        ],
        "ru": [
            ["🎟️ Мои шансы", "🔗 Моя реферальная ссылка"],
            ["📋 Правила", "🎁 Призы"],
        ],
        "en": [
            ["🎟️ My chances", "🔗 My referral link"],
            ["📋 Rules", "🎁 Prizes"],
        ]
    }

    menu = menus.get(language, menus["uz"])
    keyboard = [[KeyboardButton(text=btn) for btn in row] for row in menu]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# =============================================
# 👑 ADMIN REPLY MENU (replaces user menu for admins)
# =============================================

def get_admin_menu_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """👑 Admin reply keyboard — shown instead of user menu"""
    menus = {
        "uz": [
            ["📊 Statistika", "📥 Excel yuklab olish"],
            ["📝 Textlarni o'zgartirish", "🔄 Kanal sozlamalari"],
            ["📣 Barchaga xabar yuborish"],
        ],
        "ru": [
            ["📊 Статистика", "📥 Скачать Excel"],
            ["📝 Редактировать тексты", "🔄 Каналы"],
            ["📣 Сделать рассылку"],
        ],
        "en": [
            ["📊 Statistics", "📥 Download Excel"],
            ["📝 Edit texts", "🔄 Channel settings"],
            ["📣 Broadcast message"],
        ]
    }

    menu = menus.get(language, menus["uz"])
    keyboard = [[KeyboardButton(text=btn) for btn in row] for row in menu]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# =============================================
# 👑 ADMIN INLINE PANEL (for inline actions)
# =============================================

def get_admin_keyboard(language: str = "uz") -> InlineKeyboardMarkup:
    """👑 Admin panel inline keyboard"""
    buttons = {
        "uz": [
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📝 Textlarni o'zgartirish", callback_data="admin_edit_texts")],
            [InlineKeyboardButton(text="📥 Excel yuklab olish", callback_data="admin_export")],
            [InlineKeyboardButton(text="📣 Barchaga xabar yuborish", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔄 Kanal sozlamalari", callback_data="admin_channels")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_close")],
        ],
        "ru": [
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📝 Редактировать тексты", callback_data="admin_edit_texts")],
            [InlineKeyboardButton(text="📥 Скачать Excel", callback_data="admin_export")],
            [InlineKeyboardButton(text="📣 Сделать рассылку", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔄 Настройки каналов", callback_data="admin_channels")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_close")],
        ],
        "en": [
            [InlineKeyboardButton(text="📊 Statistics", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📝 Edit texts", callback_data="admin_edit_texts")],
            [InlineKeyboardButton(text="📥 Download Excel", callback_data="admin_export")],
            [InlineKeyboardButton(text="📣 Broadcast message", callback_data="admin_broadcast")],
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
        ("welcome", "🏠 Xush kelibsiz"),
        ("ask_contact", "📱 Kontakt so'rash"),
        ("channels_intro", "📢 Kanallar bilan tanishuv"),
        ("verification_success", "✅ Muvaffaqiyatli tasdiqlash"),
        ("code_message", "🎟️ Kod xabari"),
        ("referral_info", "🔗 Referal ma'lumoti"),
        ("referral_notification", "🔔 Referal xabarnomasi"),
        ("my_chances", "🎟️ Mening imkoniyatlarim"),
        ("rules", "📋 Qoidalar"),
        ("prizes", "🎁 Sovrinlar"),
        ("already_registered", "⚠️ Ro'yxatdan o'tgan"),
        ("not_verified", "❌ Tasdiqlanmagan"),
        ("stats_message", "📊 Bot statistikasi"),
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
