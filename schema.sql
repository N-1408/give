-- ============================================
-- 🎁 Telegram Giveaway Bot - Full Database Schema
-- 📁 File: schema.sql
-- 👤 Created by: User with AI
-- 📝 Complete Supabase PostgreSQL schema for the giveaway bot.
--    Includes users, codes, channels, dynamic texts, and settings.
--    Run this SQL in Supabase SQL Editor to initialize the database.
-- 📅 Created: 2026-03-15 07:47 (Tashkent Time)
-- ============================================
-- 📋 CHANGE LOG:
-- [2026-03-15 08:06 Tashkent] - Disabled RLS on all tables (bot uses
--   direct asyncpg connection, not Supabase client, so RLS not needed)
-- ============================================

-- =============================================
-- 👤 USERS TABLE
-- Stores all bot users with their Telegram info
-- =============================================
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,           -- 🆔 Telegram user ID
    username VARCHAR(255),                         -- 📛 @username (nullable)
    first_name VARCHAR(255),                       -- 👤 First name
    last_name VARCHAR(255),                        -- 👤 Last name
    phone VARCHAR(50),                             -- 📱 Phone number
    language VARCHAR(10) DEFAULT 'uz',             -- 🌐 Selected language
    referrer_id BIGINT,                            -- 🔗 Who referred this user (telegram_id)
    is_verified BOOLEAN DEFAULT FALSE,             -- ✅ All channels verified
    is_admin BOOLEAN DEFAULT FALSE,                -- 👑 Admin role (via /shep)
    instagram_clicked BOOLEAN DEFAULT FALSE,       -- 📸 Instagram link clicked
    youtube_clicked BOOLEAN DEFAULT FALSE,         -- ▶️ YouTube link clicked
    telegram_joined BOOLEAN DEFAULT FALSE,         -- 📢 Telegram channel joined
    created_at TIMESTAMPTZ DEFAULT NOW(),          -- 📅 Registration date
    updated_at TIMESTAMPTZ DEFAULT NOW()           -- 📅 Last update
);

-- =============================================
-- 🎟️ CODES TABLE
-- Unique participation codes for each user
-- =============================================
CREATE TABLE IF NOT EXISTS codes (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,                       -- 🆔 Owner's telegram_id
    code VARCHAR(10) UNIQUE NOT NULL,              -- 🎟️ Unique 6-char code (e.g. A3K9X2)
    code_type VARCHAR(20) NOT NULL,                -- 📋 'subscription' or 'referral'
    referred_user_id BIGINT,                       -- 🔗 Who was referred (for referral type)
    created_at TIMESTAMPTZ DEFAULT NOW(),          -- 📅 When code was issued
    CONSTRAINT fk_codes_user FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
);

-- =============================================
-- 📢 CHANNELS TABLE
-- Configurable channel links for subscription checks
-- =============================================
CREATE TABLE IF NOT EXISTS channels (
    id SERIAL PRIMARY KEY,
    channel_type VARCHAR(20) NOT NULL,             -- 📋 'telegram', 'instagram', 'youtube'
    channel_id VARCHAR(255),                       -- 🆔 Telegram channel ID (@username or numeric)
    channel_url VARCHAR(500) NOT NULL,             -- 🔗 Full URL to channel
    channel_name VARCHAR(255),                     -- 📛 Display name
    is_active BOOLEAN DEFAULT TRUE                 -- ✅ Whether this channel is active
);

-- =============================================
-- 📝 BOT TEXTS TABLE
-- Dynamic bot messages editable by admin
-- =============================================
CREATE TABLE IF NOT EXISTS bot_texts (
    id SERIAL PRIMARY KEY,
    text_key VARCHAR(100) NOT NULL,                -- 🔑 Message key (e.g. 'welcome', 'rules')
    language VARCHAR(10) NOT NULL,                 -- 🌐 Language code ('uz', 'ru', 'en')
    content TEXT NOT NULL,                         -- 📝 Message content
    image_file_id VARCHAR(255),                    -- 🖼️ Telegram file_id for attached image
    updated_at TIMESTAMPTZ DEFAULT NOW(),          -- 📅 Last edit timestamp
    UNIQUE(text_key, language)                     -- 🔐 One text per key+language
);

-- =============================================
-- ⚙️ BOT SETTINGS TABLE
-- Key-value store for bot configuration
-- =============================================
CREATE TABLE IF NOT EXISTS bot_settings (
    key VARCHAR(100) PRIMARY KEY,                  -- 🔑 Setting name
    value TEXT NOT NULL,                            -- 📝 Setting value
    updated_at TIMESTAMPTZ DEFAULT NOW()           -- 📅 Last update
);

-- =============================================
-- 📊 INDEXES for Performance
-- Critical for 500K+ users and fast queries
-- =============================================
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_referrer_id ON users(referrer_id);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_codes_user_id ON codes(user_id);
CREATE INDEX IF NOT EXISTS idx_codes_code ON codes(code);
CREATE INDEX IF NOT EXISTS idx_bot_texts_key_lang ON bot_texts(text_key, language);

-- =============================================
-- � DISABLE ROW LEVEL SECURITY
-- Bot uses direct asyncpg connection (not Supabase client)
-- RLS is not needed and causes false Security Advisor warnings
-- =============================================
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE codes DISABLE ROW LEVEL SECURITY;
ALTER TABLE channels DISABLE ROW LEVEL SECURITY;
ALTER TABLE bot_texts DISABLE ROW LEVEL SECURITY;
ALTER TABLE bot_settings DISABLE ROW LEVEL SECURITY;

-- =============================================
-- �📢 DEFAULT CHANNEL DATA
-- Pre-populate channels
-- =============================================
INSERT INTO channels (channel_type, channel_id, channel_url, channel_name, is_active) VALUES
    ('telegram', '@aliypubgm', 'https://t.me/aliypubgm', 'Aliy PUBGM', TRUE),
    ('instagram', NULL, 'https://www.instagram.com/aliypubgm_', 'aliypubgm_', TRUE),
    ('youtube', NULL, 'https://www.youtube.com/@aliypubgm', 'Aliy PUBGM', TRUE)
ON CONFLICT DO NOTHING;

-- =============================================
-- 📝 DEFAULT BOT TEXTS
-- Pre-populate with default messages in 3 languages
-- =============================================

-- 🌐 UZBEK DEFAULTS
INSERT INTO bot_texts (text_key, language, content) VALUES
    ('welcome', 'uz', '🎁 *Giveaway Botga xush kelibsiz!*

Sovg''alarni yutib olish imkoniyatini qo''lga kiriting! Quyidagi oddiy qadamlarni bajaring va o''yinda ishtirok eting.'),
    ('ask_contact', 'uz', '📱 Iltimos, telefon raqamingizni yuboring.

Quyidagi tugmani bosing:'),
    ('channels_intro', 'uz', '📢 *Kanallarimizga obuna bo''ling!*

Barcha kanallarga obuna bo''lganingizdan so''ng "✅ Tekshirish" tugmasini bosing.'),
    ('verification_success', 'uz', '🎉 *Tabriklaymiz!*

Siz muvaffaqiyatli ro''yxatdan o''tdingiz va giveaway''da ishtirok etish uchun maxsus kod oldingiz!'),
    ('code_message', 'uz', '🎟️ *Sizning maxsus kodingiz:* `{code}`

🔗 *Referal havolangiz:* `{referral_link}`

Do''stlaringizni taklif qiling va qo''shimcha kodlar yutib oling! Har bir do''stingiz uchun +1 imkoniyat! 🚀'),
    ('referral_info', 'uz', '🔗 *Sizning referal havolangiz:*
`{referral_link}`

Havolani do''stlaringizga yuboring. Har bir do''stingiz ro''yxatdan o''tsa, siz yana bitta maxsus kod olasiz!'),
    ('referral_notification', 'uz', '🎉 *Yangi referal!*

👤 *{name}* ismli foydalanuvchi sizning havolangiz orqali ro''yxatdan o''tdi!
🎟️ Sizga yangi kod berildi: `{code}`
📊 Jami imkoniyatlar: *{total} ta*'),
    ('my_chances', 'uz', '🎟️ *Mening imkoniyatlarim*

📊 Jami kodlar: *{total} ta*
🎫 Obuna kodi: 1 ta
🔗 Referal kodlari: *{referral_count} ta*

Kodlaringiz:
{codes_list}'),
    ('rules', 'uz', '📋 *Giveaway Qoidalari*

1️⃣ Telegram kanalga obuna bo''ling
2️⃣ Instagram va YouTube kanallarni kuzating
3️⃣ "Tekshirish" tugmasini bosing
4️⃣ Maxsus kodingizni qo''lga kiriting
5️⃣ Do''stlaringizni taklif qilib qo''shimcha kodlar oling

⚠️ *Muhim:* Giveaway yakunlangach kodlar tasodifiy tanlanadi. Ko''proq kod = ko''proq imkoniyat!

📅 Giveaway sanasi e''lon qilinadi.'),
    ('prizes', 'uz', '🎁 *Sovg''alar*

🥇 1-o''rin: Tez orada e''lon qilinadi
🥈 2-o''rin: Tez orada e''lon qilinadi
🥉 3-o''rin: Tez orada e''lon qilinadi

📢 Sovg''alar ro''yxati yangilanishi mumkin. Kuzatib boring!'),
    ('contact_admin', 'uz', '📩 *Adminga murojaat*

Savollaringiz bo''lsa, adminga yozing:
@aliy_admin'),
    ('already_registered', 'uz', '⚠️ Siz allaqachon ro''yxatdan o''tgansiz!

Asosiy menyudan foydalaning:'),
    ('not_verified', 'uz', '❌ *Barcha kanallarni tekshiring!*

Quyidagi kanallarga obuna bo''lmagansiz:
{missing_channels}

Obuna bo''lib, qayta "✅ Tekshirish" tugmasini bosing.'),
    ('top_referrers', 'uz', '🏆 *Top Referallar*

{leaderboard}'),
    ('broadcast_confirm', 'uz', '📢 Xabar barcha foydalanuvchilarga yuborilsinmi?\n\n{message}')
ON CONFLICT (text_key, language) DO NOTHING;

-- 🌐 RUSSIAN DEFAULTS
INSERT INTO bot_texts (text_key, language, content) VALUES
    ('welcome', 'ru', '🎁 *Добро пожаловать в Giveaway Bot!*

Получите шанс выиграть призы! Выполните простые шаги и участвуйте в розыгрыше.'),
    ('ask_contact', 'ru', '📱 Пожалуйста, отправьте свой номер телефона.

Нажмите кнопку ниже:'),
    ('channels_intro', 'ru', '📢 *Подпишитесь на наши каналы!*

После подписки на все каналы нажмите кнопку "✅ Проверить".'),
    ('verification_success', 'ru', '🎉 *Поздравляем!*

Вы успешно зарегистрированы и получили уникальный код для участия в розыгрыше!'),
    ('code_message', 'ru', '🎟️ *Ваш уникальный код:* `{code}`

🔗 *Ваша реферальная ссылка:* `{referral_link}`

Приглашайте друзей и получайте дополнительные коды! +1 шанс за каждого друга! 🚀'),
    ('referral_info', 'ru', '🔗 *Ваша реферальная ссылка:*
`{referral_link}`

Отправьте ссылку друзьям. За каждого зарегистрированного друга вы получаете дополнительный код!'),
    ('referral_notification', 'ru', '🎉 *Новый реферал!*

👤 Пользователь *{name}* зарегистрировался по вашей ссылке!
🎟️ Вам выдан новый код: `{code}`
📊 Всего шансов: *{total}*'),
    ('my_chances', 'ru', '🎟️ *Мои шансы*

📊 Всего кодов: *{total}*
🎫 Код за подписку: 1
🔗 Реферальные коды: *{referral_count}*

Ваши коды:
{codes_list}'),
    ('rules', 'ru', '📋 *Правила Giveaway*

1️⃣ Подпишитесь на Telegram канал
2️⃣ Подпишитесь на Instagram и YouTube
3️⃣ Нажмите кнопку "Проверить"
4️⃣ Получите уникальный код
5️⃣ Приглашайте друзей для дополнительных кодов

⚠️ *Важно:* После завершения розыгрыша коды выбираются случайно. Больше кодов = больше шансов!

📅 Дата розыгрыша будет объявлена.'),
    ('prizes', 'ru', '🎁 *Призы*

🥇 1 место: Скоро будет объявлено
🥈 2 место: Скоро будет объявлено
🥉 3 место: Скоро будет объявлено

📢 Список призов может обновляться. Следите за новостями!'),
    ('contact_admin', 'ru', '📩 *Связаться с админом*

Если у вас есть вопросы, напишите:
@aliy_admin'),
    ('already_registered', 'ru', '⚠️ Вы уже зарегистрированы!

Используйте главное меню:'),
    ('not_verified', 'ru', '❌ *Проверьте все каналы!*

Вы не подписаны на:
{missing_channels}

Подпишитесь и снова нажмите "✅ Проверить".'),
    ('top_referrers', 'ru', '🏆 *Топ Рефералы*

{leaderboard}'),
    ('broadcast_confirm', 'ru', '📢 Отправить сообщение всем пользователям?\n\n{message}')
ON CONFLICT (text_key, language) DO NOTHING;

-- 🌐 ENGLISH DEFAULTS
INSERT INTO bot_texts (text_key, language, content) VALUES
    ('welcome', 'en', '🎁 *Welcome to Giveaway Bot!*

Get a chance to win amazing prizes! Complete simple steps and participate in the giveaway.'),
    ('ask_contact', 'en', '📱 Please share your phone number.

Tap the button below:'),
    ('channels_intro', 'en', '📢 *Subscribe to our channels!*

After subscribing to all channels, tap the "✅ Verify" button.'),
    ('verification_success', 'en', '🎉 *Congratulations!*

You''ve successfully registered and received your unique code for the giveaway!'),
    ('code_message', 'en', '🎟️ *Your unique code:* `{code}`

🔗 *Your referral link:* `{referral_link}`

Invite friends and earn more codes! +1 chance per friend! 🚀'),
    ('referral_info', 'en', '🔗 *Your referral link:*
`{referral_link}`

Share with friends. For each friend who registers, you get an additional code!'),
    ('referral_notification', 'en', '🎉 *New referral!*

👤 *{name}* registered through your link!
🎟️ New code issued: `{code}`
📊 Total chances: *{total}*'),
    ('my_chances', 'en', '🎟️ *My Chances*

📊 Total codes: *{total}*
🎫 Subscription code: 1
🔗 Referral codes: *{referral_count}*

Your codes:
{codes_list}'),
    ('rules', 'en', '📋 *Giveaway Rules*

1️⃣ Subscribe to Telegram channel
2️⃣ Follow Instagram and YouTube
3️⃣ Tap the "Verify" button
4️⃣ Get your unique code
5️⃣ Invite friends for bonus codes

⚠️ *Important:* After the giveaway ends, codes are selected randomly. More codes = more chances!

📅 Giveaway date will be announced.'),
    ('prizes', 'en', '🎁 *Prizes*

🥇 1st place: Coming soon
🥈 2nd place: Coming soon
🥉 3rd place: Coming soon

📢 Prize list may be updated. Stay tuned!'),
    ('contact_admin', 'en', '📩 *Contact Admin*

If you have questions, reach out to:
@aliy_admin'),
    ('already_registered', 'en', '⚠️ You are already registered!

Use the main menu:'),
    ('not_verified', 'en', '❌ *Check all channels!*

You haven''t subscribed to:
{missing_channels}

Subscribe and tap "✅ Verify" again.'),
    ('top_referrers', 'en', '🏆 *Top Referrers*

{leaderboard}'),
    ('broadcast_confirm', 'en', '📢 Send this message to all users?\n\n{message}')
ON CONFLICT (text_key, language) DO NOTHING;
