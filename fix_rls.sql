-- ============================================
-- 🎁 Telegram Giveaway Bot - FIX SQL
-- 📁 File: fix_rls.sql
-- 👤 Created by: User with AI
-- 📝 Run this in Supabase SQL Editor to fix RLS errors.
--    Drops ALL old tables and recreates them properly
--    with RLS enabled and correct policies.
-- 📅 Created: 2026-03-15 08:26 (Tashkent Time)
-- ============================================

-- ⚠️ DROP ALL OLD TABLES (clean start)
DROP TABLE IF EXISTS codes CASCADE;
DROP TABLE IF EXISTS bot_texts CASCADE;
DROP TABLE IF EXISTS bot_settings CASCADE;
DROP TABLE IF EXISTS channels CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- =============================================
-- 👤 USERS TABLE
-- =============================================
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone VARCHAR(50),
    language VARCHAR(10) DEFAULT 'uz',
    referrer_id BIGINT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    instagram_clicked BOOLEAN DEFAULT FALSE,
    youtube_clicked BOOLEAN DEFAULT FALSE,
    telegram_joined BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- 🎟️ CODES TABLE
-- =============================================
CREATE TABLE codes (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL,
    code_type VARCHAR(20) NOT NULL,
    referred_user_id BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_codes_user FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
);

-- =============================================
-- 📢 CHANNELS TABLE
-- =============================================
CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    channel_type VARCHAR(20) NOT NULL,
    channel_id VARCHAR(255),
    channel_url VARCHAR(500) NOT NULL,
    channel_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
);

-- =============================================
-- 📝 BOT TEXTS TABLE
-- =============================================
CREATE TABLE bot_texts (
    id SERIAL PRIMARY KEY,
    text_key VARCHAR(100) NOT NULL,
    language VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    image_file_id VARCHAR(255),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(text_key, language)
);

-- =============================================
-- ⚙️ BOT SETTINGS TABLE
-- =============================================
CREATE TABLE bot_settings (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- 🔐 ROW LEVEL SECURITY — ENABLE + POLICIES
-- This fixes the Security Advisor errors properly:
-- RLS is ON (tables protected from PostgREST anon access)
-- Policies allow postgres role (asyncpg direct connection)
-- =============================================

-- 👤 users
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_all_users" ON users
    FOR ALL TO postgres, service_role
    USING (true) WITH CHECK (true);

-- 🎟️ codes
ALTER TABLE codes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_all_codes" ON codes
    FOR ALL TO postgres, service_role
    USING (true) WITH CHECK (true);

-- 📢 channels
ALTER TABLE channels ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_all_channels" ON channels
    FOR ALL TO postgres, service_role
    USING (true) WITH CHECK (true);

-- 📝 bot_texts
ALTER TABLE bot_texts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_all_bot_texts" ON bot_texts
    FOR ALL TO postgres, service_role
    USING (true) WITH CHECK (true);

-- ⚙️ bot_settings
ALTER TABLE bot_settings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_all_bot_settings" ON bot_settings
    FOR ALL TO postgres, service_role
    USING (true) WITH CHECK (true);

-- =============================================
-- 📊 INDEXES
-- =============================================
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_users_referrer_id ON users(referrer_id);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_codes_user_id ON codes(user_id);
CREATE INDEX idx_codes_code ON codes(code);
CREATE INDEX idx_bot_texts_key_lang ON bot_texts(text_key, language);

-- =============================================
-- 📢 DEFAULT CHANNELS (makemarketing_uz vaqtinchalik)
-- =============================================
INSERT INTO channels (channel_type, channel_id, channel_url, channel_name, is_active) VALUES
    ('telegram', '@makemarketing_uz', 'https://t.me/makemarketing_uz', 'Make Marketing UZ', TRUE),
    ('instagram', NULL, 'https://www.instagram.com/aliypubgm_', 'aliypubgm_', TRUE),
    ('youtube', NULL, 'https://www.youtube.com/@aliypubgm', 'Aliy PUBGM', TRUE);

-- =============================================
-- 📝 DEFAULT BOT TEXTS — UZBEK
-- =============================================
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
    ('broadcast_confirm', 'uz', '📢 Xabar barcha foydalanuvchilarga yuborilsinmi?\n\n{message}');

-- =============================================
-- 📝 DEFAULT BOT TEXTS — RUSSIAN
-- =============================================
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
    ('broadcast_confirm', 'ru', '📢 Отправить сообщение всем пользователям?\n\n{message}');

-- =============================================
-- 📝 DEFAULT BOT TEXTS — ENGLISH
-- =============================================
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
    ('broadcast_confirm', 'en', '📢 Send this message to all users?\n\n{message}');
