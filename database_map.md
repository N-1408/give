# ============================================
# 🗄️ Database Map - Telegram Giveaway Bot
# 📁 File: database_map.md
# 👤 Created by: User with AI
# 📝 Complete database structure documentation.
#    This file maps all tables, columns, and their purposes.
#    Keep this updated when modifying the database schema.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

# 🗄️ Database Map

## Platform: Supabase (PostgreSQL)

---

## 📋 Tables Overview

| Table | Purpose | Est. Rows |
|-------|---------|-----------|
| `users` | All bot users with Telegram info | 500,000+ |
| `codes` | Unique participation codes | 600,000+ |
| `channels` | Channel links for subscription checks | 3-5 |
| `bot_texts` | Dynamic bot messages (admin-editable) | ~45 |
| `bot_settings` | Key-value config store | ~10 |

---

## 👤 `users` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL PK | Auto-increment ID |
| `telegram_id` | BIGINT UNIQUE | Telegram user ID |
| `username` | VARCHAR(255) | @username (nullable) |
| `first_name` | VARCHAR(255) | First name |
| `last_name` | VARCHAR(255) | Last name |
| `phone` | VARCHAR(50) | Phone number |
| `language` | VARCHAR(10) | Selected language (uz/ru/en) |
| `referrer_id` | BIGINT | Referrer's telegram_id |
| `is_verified` | BOOLEAN | All channels verified |
| `is_admin` | BOOLEAN | Admin role (via /shep) |
| `instagram_clicked` | BOOLEAN | Instagram link clicked |
| `youtube_clicked` | BOOLEAN | YouTube link clicked |
| `telegram_joined` | BOOLEAN | Telegram channel joined |
| `created_at` | TIMESTAMPTZ | Registration date |
| `updated_at` | TIMESTAMPTZ | Last update |

## 🎟️ `codes` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL PK | Auto-increment ID |
| `user_id` | BIGINT FK→users | Owner's telegram_id |
| `code` | VARCHAR(10) UNIQUE | 6-char alphanumeric code |
| `code_type` | VARCHAR(20) | 'subscription' or 'referral' |
| `referred_user_id` | BIGINT | Who was referred (for referral type) |
| `created_at` | TIMESTAMPTZ | When code was issued |

## 📢 `channels` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Auto-increment ID |
| `channel_type` | VARCHAR(20) | 'telegram', 'instagram', 'youtube' |
| `channel_id` | VARCHAR(255) | Telegram channel ID for API check |
| `channel_url` | VARCHAR(500) | Full URL to channel |
| `channel_name` | VARCHAR(255) | Display name |
| `is_active` | BOOLEAN | Whether channel is active |

## 📝 `bot_texts` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Auto-increment ID |
| `text_key` | VARCHAR(100) | Message key (e.g. 'welcome') |
| `language` | VARCHAR(10) | Language code (uz/ru/en) |
| `content` | TEXT | Message content (supports Markdown) |
| `image_file_id` | VARCHAR(255) | Telegram file_id for attached image |
| `updated_at` | TIMESTAMPTZ | Last edit timestamp |

### Text Keys:
`welcome`, `ask_contact`, `channels_intro`, `verification_success`, `code_message`, `referral_info`, `referral_notification`, `my_chances`, `rules`, `prizes`, `contact_admin`, `already_registered`, `not_verified`, `top_referrers`, `broadcast_confirm`

## ⚙️ `bot_settings` Table

| Column | Type | Description |
|--------|------|-------------|
| `key` | VARCHAR(100) PK | Setting name |
| `value` | TEXT | Setting value |
| `updated_at` | TIMESTAMPTZ | Last update |
