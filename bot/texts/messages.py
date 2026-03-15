# ============================================
# 📝 Messages Module - Telegram Giveaway Bot
# 📁 File: bot/texts/messages.py
# 👤 Created by: User with AI
# 📝 Provides bot text retrieval with database-first approach.
#    Falls back to hardcoded defaults if DB text is not found.
#    Supports dynamic placeholders like {code}, {referral_link}, etc.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

import logging
from typing import Optional
from bot import database as db

logger = logging.getLogger(__name__)

# =============================================
# 🔤 FALLBACK MESSAGES (used if DB is empty)
# =============================================
FALLBACK_MESSAGES = {
    # 🇺🇿 Uzbek
    "uz": {
        "welcome": "🎁 *Giveaway Botga xush kelibsiz!*\n\nSovg'alarni yutib olish imkoniyatini qo'lga kiriting!",
        "ask_contact": "📱 Iltimos, telefon raqamingizni yuboring.\n\nQuyidagi tugmani bosing:",
        "channels_intro": "📢 *Kanallarimizga obuna bo'ling!*\n\nBarcha kanallarga obuna bo'lganingizdan so'ng \"✅ Tekshirish\" tugmasini bosing.",
        "verification_success": "🎉 *Tabriklaymiz!*\n\nSiz muvaffaqiyatli ro'yxatdan o'tdingiz!",
        "code_message": "🎟️ *Sizning maxsus kodingiz:* `{code}`\n\n🔗 *Referal havolangiz:* `{referral_link}`\n\nDo'stlaringizni taklif qiling va qo'shimcha kodlar yutib oling! 🚀",
        "referral_info": "🔗 *Sizning referal havolangiz:*\n`{referral_link}`\n\nHar bir do'stingiz ro'yxatdan o'tsa, siz yana bitta maxsus kod olasiz!",
        "referral_notification": "🎉 *Yangi referal!*\n\n👤 *{name}* ismli foydalanuvchi sizning havolangiz orqali ro'yxatdan o'tdi!\n🎟️ Sizga yangi kod berildi: `{code}`\n📊 Jami imkoniyatlar: *{total} ta*",
        "my_chances": "🎟️ *Mening imkoniyatlarim*\n\n📊 Jami kodlar: *{total} ta*\n🎫 Obuna kodi: 1 ta\n🔗 Referal kodlari: *{referral_count} ta*\n\nKodlaringiz:\n{codes_list}",
        "rules": "📋 *Giveaway Qoidalari*\n\n1️⃣ Telegram kanalga obuna bo'ling\n2️⃣ Instagram va YouTube kanallarni kuzating\n3️⃣ \"Tekshirish\" tugmasini bosing\n4️⃣ Maxsus kodingizni qo'lga kiriting\n5️⃣ Do'stlaringizni taklif qilib qo'shimcha kodlar oling\n\n⚠️ *Muhim:* Ko'proq kod = ko'proq imkoniyat!",
        "prizes": "🎁 *Sovg'alar*\n\n🥇 1-o'rin: Tez orada e'lon qilinadi\n🥈 2-o'rin: Tez orada e'lon qilinadi\n🥉 3-o'rin: Tez orada e'lon qilinadi",
        "contact_admin": "📩 *Adminga murojaat*\n\nSavollaringiz bo'lsa, adminga yozing:\n@aliy_admin",
        "already_registered": "⚠️ Siz allaqachon ro'yxatdan o'tgansiz!\n\nAsosiy menyudan foydalaning:",
        "not_verified": "❌ *Barcha kanallarni tekshiring!*\n\nQuyidagi kanallarga obuna bo'lmagansiz:\n{missing_channels}",
        "top_referrers": "🏆 *Top Referallar*\n\n{leaderboard}",
        "choose_language": "🌐 *Tilni tanlang / Выберите язык / Choose language:*",
        "wrong_password": "❌ Parol noto'g'ri!",
        "admin_welcome": "👑 *Admin Panel*\n\nXush kelibsiz, admin!",
        "enter_password": "🔐 Parolni kiriting:",
        "broadcast_confirm": "📢 Xabar barcha foydalanuvchilarga yuborilsinmi?",
        "broadcast_started": "📢 Xabar yuborish boshlandi...\n📊 Jami: {total} ta foydalanuvchi",
        "broadcast_done": "✅ Xabar yuborish yakunlandi!\n\n📤 Yuborildi: {sent}\n❌ Xato: {failed}\n🚫 Bloklangan: {blocked}",
        "select_text_key": "📝 Qaysi textni o'zgartirmoqchisiz?",
        "select_language": "🌐 Qaysi til uchun o'zgartirasiz?",
        "send_new_text": "📝 Yangi textni yuboring:\n\n(Rasm biriktirmoqchi bo'lsangiz, rasmga caption sifatida textni yozing)",
        "text_updated": "✅ Text muvaffaqiyatli yangilandi!",
        "stats_message": "📊 *Bot Statistikasi*\n\n👥 *Foydalanuvchilar:*\n├ Bugungi: {today_users}\n├ Jami: {total_users}\n├ Tasdiqlangan: {verified_users}\n└ Bugun tasdiqlangan: {today_verified}\n\n🎟️ *Kodlar:*\n├ Bugungi: {today_codes}\n├ Jami: {total_codes}\n├ Obuna kodlari: {subscription_codes}\n├ Referal kodlari: {referral_codes}\n└ Bugun referal: {today_referral_codes}",
        "export_generating": "📥 Excel fayl tayyorlanmoqda...",
        "export_done": "✅ Excel fayl tayyor!",
        "send_broadcast_text": "📢 Barcha foydalanuvchilarga yuboriladigan xabarni yozing:\n\n(Rasm biriktirmoqchi bo'lsangiz, rasmga caption sifatida textni yozing)",
    },
    # 🇷🇺 Russian
    "ru": {
        "welcome": "🎁 *Добро пожаловать в Giveaway Bot!*\n\nПолучите шанс выиграть призы!",
        "ask_contact": "📱 Пожалуйста, отправьте свой номер телефона.\n\nНажмите кнопку ниже:",
        "channels_intro": "📢 *Подпишитесь на наши каналы!*\n\nПосле подписки на все каналы нажмите \"✅ Проверить\".",
        "verification_success": "🎉 *Поздравляем!*\n\nВы успешно зарегистрированы!",
        "code_message": "🎟️ *Ваш уникальный код:* `{code}`\n\n🔗 *Ваша реферальная ссылка:* `{referral_link}`\n\nПриглашайте друзей и получайте дополнительные коды! 🚀",
        "referral_info": "🔗 *Ваша реферальная ссылка:*\n`{referral_link}`\n\nЗа каждого зарегистрированного друга вы получаете дополнительный код!",
        "referral_notification": "🎉 *Новый реферал!*\n\n👤 Пользователь *{name}* зарегистрировался по вашей ссылке!\n🎟️ Вам выдан новый код: `{code}`\n📊 Всего шансов: *{total}*",
        "my_chances": "🎟️ *Мои шансы*\n\n📊 Всего кодов: *{total}*\n🎫 Код за подписку: 1\n🔗 Реферальные коды: *{referral_count}*\n\nВаши коды:\n{codes_list}",
        "rules": "📋 *Правила Giveaway*\n\n1️⃣ Подпишитесь на Telegram канал\n2️⃣ Подпишитесь на Instagram и YouTube\n3️⃣ Нажмите кнопку \"Проверить\"\n4️⃣ Получите уникальный код\n5️⃣ Приглашайте друзей для дополнительных кодов\n\n⚠️ *Важно:* Больше кодов = больше шансов!",
        "prizes": "🎁 *Призы*\n\n🥇 1 место: Скоро будет объявлено\n🥈 2 место: Скоро будет объявлено\n🥉 3 место: Скоро будет объявлено",
        "contact_admin": "📩 *Связаться с админом*\n\nНапишите:\n@aliy_admin",
        "already_registered": "⚠️ Вы уже зарегистрированы!\n\nИспользуйте главное меню:",
        "not_verified": "❌ *Проверьте все каналы!*\n\nВы не подписаны на:\n{missing_channels}",
        "top_referrers": "🏆 *Топ Рефералы*\n\n{leaderboard}",
        "choose_language": "🌐 *Tilni tanlang / Выберите язык / Choose language:*",
        "wrong_password": "❌ Неверный пароль!",
        "admin_welcome": "👑 *Админ-панель*\n\nДобро пожаловать, админ!",
        "enter_password": "🔐 Введите пароль:",
        "broadcast_confirm": "📢 Отправить сообщение всем пользователям?",
        "broadcast_started": "📢 Отправка начата...\n📊 Всего: {total} пользователей",
        "broadcast_done": "✅ Отправка завершена!\n\n📤 Отправлено: {sent}\n❌ Ошибок: {failed}\n🚫 Заблокировано: {blocked}",
        "select_text_key": "📝 Какой текст вы хотите изменить?",
        "select_language": "🌐 Для какого языка?",
        "send_new_text": "📝 Отправьте новый текст:\n\n(Чтобы прикрепить изображение, напишите текст как подпись к фото)",
        "text_updated": "✅ Текст успешно обновлён!",
        "stats_message": "📊 *Статистика бота*\n\n👥 *Пользователи:*\n├ Сегодня: {today_users}\n├ Всего: {total_users}\n├ Подтверждено: {verified_users}\n└ Сегодня подтверждено: {today_verified}\n\n🎟️ *Коды:*\n├ Сегодня: {today_codes}\n├ Всего: {total_codes}\n├ За подписку: {subscription_codes}\n├ Реферальные: {referral_codes}\n└ Сегодня реферальные: {today_referral_codes}",
        "export_generating": "📥 Генерация Excel файла...",
        "export_done": "✅ Excel файл готов!",
        "send_broadcast_text": "📢 Напишите сообщение для всех пользователей:\n\n(Чтобы прикрепить изображение, напишите текст как подпись к фото)",
    },
    # 🇬🇧 English
    "en": {
        "welcome": "🎁 *Welcome to Giveaway Bot!*\n\nGet a chance to win amazing prizes!",
        "ask_contact": "📱 Please share your phone number.\n\nTap the button below:",
        "channels_intro": "📢 *Subscribe to our channels!*\n\nAfter subscribing, tap \"✅ Verify\".",
        "verification_success": "🎉 *Congratulations!*\n\nYou've successfully registered!",
        "code_message": "🎟️ *Your unique code:* `{code}`\n\n🔗 *Your referral link:* `{referral_link}`\n\nInvite friends and earn more codes! 🚀",
        "referral_info": "🔗 *Your referral link:*\n`{referral_link}`\n\nFor each friend who registers, you get an additional code!",
        "referral_notification": "🎉 *New referral!*\n\n👤 *{name}* registered through your link!\n🎟️ New code issued: `{code}`\n📊 Total chances: *{total}*",
        "my_chances": "🎟️ *My Chances*\n\n📊 Total codes: *{total}*\n🎫 Subscription code: 1\n🔗 Referral codes: *{referral_count}*\n\nYour codes:\n{codes_list}",
        "rules": "📋 *Giveaway Rules*\n\n1️⃣ Subscribe to Telegram channel\n2️⃣ Follow Instagram and YouTube\n3️⃣ Tap \"Verify\"\n4️⃣ Get your unique code\n5️⃣ Invite friends for bonus codes\n\n⚠️ *Important:* More codes = more chances!",
        "prizes": "🎁 *Prizes*\n\n🥇 1st: Coming soon\n🥈 2nd: Coming soon\n🥉 3rd: Coming soon",
        "contact_admin": "📩 *Contact Admin*\n\nReach out to:\n@aliy_admin",
        "already_registered": "⚠️ You are already registered!\n\nUse the main menu:",
        "not_verified": "❌ *Check all channels!*\n\nYou haven't subscribed to:\n{missing_channels}",
        "top_referrers": "🏆 *Top Referrers*\n\n{leaderboard}",
        "choose_language": "🌐 *Tilni tanlang / Выберите язык / Choose language:*",
        "wrong_password": "❌ Wrong password!",
        "admin_welcome": "👑 *Admin Panel*\n\nWelcome, admin!",
        "enter_password": "🔐 Enter password:",
        "broadcast_confirm": "📢 Send message to all users?",
        "broadcast_started": "📢 Broadcast started...\n📊 Total: {total} users",
        "broadcast_done": "✅ Broadcast completed!\n\n📤 Sent: {sent}\n❌ Failed: {failed}\n🚫 Blocked: {blocked}",
        "select_text_key": "📝 Which text do you want to edit?",
        "select_language": "🌐 For which language?",
        "send_new_text": "📝 Send the new text:\n\n(To attach an image, write the text as a photo caption)",
        "text_updated": "✅ Text updated successfully!",
        "stats_message": "📊 *Bot Statistics*\n\n👥 *Users:*\n├ Today: {today_users}\n├ Total: {total_users}\n├ Verified: {verified_users}\n└ Today verified: {today_verified}\n\n🎟️ *Codes:*\n├ Today: {today_codes}\n├ Total: {total_codes}\n├ Subscription: {subscription_codes}\n├ Referral: {referral_codes}\n└ Today referral: {today_referral_codes}",
        "export_generating": "📥 Generating Excel file...",
        "export_done": "✅ Excel file is ready!",
        "send_broadcast_text": "📢 Write the message for all users:\n\n(To attach an image, write the text as a photo caption)",
    }
}


async def get_message(text_key: str, language: str = "uz", **kwargs) -> str:
    """
    📝 Get a bot message with DB-first, fallback approach

    1. Try to get from database (admin-editable)
    2. Fall back to hardcoded defaults
    3. Apply format kwargs (e.g. {code}, {referral_link})
    """
    # 🗄️ Try database first
    try:
        db_text = await db.get_text(text_key, language)
        if db_text and db_text.get("content"):
            text = db_text["content"]
            if kwargs:
                try:
                    text = text.format(**kwargs)
                except (KeyError, IndexError):
                    pass
            return text
    except Exception as e:
        logger.warning(f"⚠️ DB text fetch failed for {text_key}/{language}: {e}")

    # 📋 Fallback to hardcoded defaults
    lang_messages = FALLBACK_MESSAGES.get(language, FALLBACK_MESSAGES["uz"])
    text = lang_messages.get(text_key, f"[{text_key}]")

    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass

    return text


async def get_text_with_image(text_key: str, language: str = "uz") -> tuple:
    """
    🖼️ Get text + image_file_id from database

    Returns:
        tuple: (content_str, image_file_id_or_None)
    """
    try:
        db_text = await db.get_text(text_key, language)
        if db_text:
            return db_text.get("content", ""), db_text.get("image_file_id")
    except Exception as e:
        logger.warning(f"⚠️ DB text fetch failed: {e}")

    lang_messages = FALLBACK_MESSAGES.get(language, FALLBACK_MESSAGES["uz"])
    return lang_messages.get(text_key, f"[{text_key}]"), None
