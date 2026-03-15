# ============================================
# 🗄️ Database Module - Telegram Giveaway Bot
# 📁 File: bot/database.py
# 👤 Created by: User with AI
# 📝 Handles all database operations via asyncpg for Supabase.
#    Uses connection pooling for efficient async queries.
#    Provides CRUD operations for users, codes, texts, and channels.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================
# 📋 CHANGE LOG:
# [2026-03-15 08:26 Tashkent] - Added full channel management
# [2026-03-15 09:56 Tashkent] - Fixed `referrer_id` on conflict in DB.
# ============================================
import os
import asyncpg
import asyncio
import logging
from typing import List, Optional, Any
from datetime import datetime, timedelta, timezone

from bot.config import config

logger = logging.getLogger(__name__)

# =============================================
# 🗄️ DATABASE CONNECTION POOL
# =============================================
_pool = None


async def get_pool():
    """🔌 Get or create the asyncpg connection pool with SSL and retry logic"""
    global _pool
    if _pool is None:
        import ssl
        
        def _create_ssl_context():
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            return ctx

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                _pool = await asyncpg.create_pool(
                    dsn=config.SUPABASE_DB_URL,
                    min_size=1,
                    max_size=5,
                    command_timeout=60,
                    ssl=_create_ssl_context(),
                    statement_cache_size=0, # MUST be 0 for Supabase Session Pooler
                )
                logger.info("✅ Database connection pool created successfully")
                break
            except Exception as e:
                logger.warning(f"⚠️ DB connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error("❌ Final DB connection attempt failed")
                    raise e
    return _pool


async def init_db():
    """🗄️ Initialize database connection"""
    await get_pool()


async def close_db():
    """🔌 Close database connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("🔌 Database connection pool closed")


# =============================================
# 👤 USER OPERATIONS
# =============================================

async def save_user(
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone: Optional[str] = None,
    language: str = "uz",
    referrer_id: Optional[int] = None
) -> dict:
    """💾 Save or update a user in the database"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO users (telegram_id, username, first_name, last_name, phone, language, referrer_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (telegram_id) DO UPDATE SET
                username = COALESCE($2, users.username),
                first_name = COALESCE($3, users.first_name),
                last_name = COALESCE($4, users.last_name),
                phone = COALESCE($5, users.phone),
                language = $6,
                referrer_id = COALESCE(users.referrer_id, $7),
                updated_at = NOW()
            RETURNING *
        """, telegram_id, username, first_name, last_name, phone, language, referrer_id)
        return dict(row) if row else {}


async def get_user(telegram_id: int) -> Optional[dict]:
    """🔍 Fetch a user by their Telegram ID"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1", telegram_id
        )
        return dict(row) if row else None


async def update_user_field(telegram_id: int, field: str, value: Any):
    """✏️ Update a single field for a user"""
    pool = await get_pool()
    # ⚠️ Whitelist of allowed fields for safety
    allowed_fields = [
        "username", "first_name", "last_name", "phone", "language",
        "is_verified", "is_admin", "instagram_clicked", "youtube_clicked",
        "telegram_joined", "referrer_id"
    ]
    if field not in allowed_fields:
        raise ValueError(f"Field '{field}' is not allowed")
    async with pool.acquire() as conn:
        await conn.execute(
            f"UPDATE users SET {field} = $1, updated_at = NOW() WHERE telegram_id = $2",
            value, telegram_id
        )


async def set_admin(telegram_id: int, is_admin: bool = True):
    """👑 Set or remove admin role for a user"""
    await update_user_field(telegram_id, "is_admin", is_admin)


async def is_user_admin(telegram_id: int) -> bool:
    """👑 Check if a user is an admin"""
    user = await get_user(telegram_id)
    return user.get("is_admin", False) if user else False


async def get_all_user_ids() -> List[int]:
    """📋 Get all user Telegram IDs (for broadcast)"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT telegram_id FROM users ORDER BY id")
        return [row["telegram_id"] for row in rows]


async def get_all_users_for_export() -> List[dict]:
    """📥 Get all users with their codes for Excel export"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT 
                u.telegram_id,
                u.username,
                u.first_name,
                u.last_name,
                u.phone,
                u.language,
                u.is_verified,
                u.created_at,
                COALESCE(
                    (SELECT string_agg(c.code, ', ' ORDER BY c.created_at)
                     FROM codes c WHERE c.user_id = u.telegram_id), ''
                ) as codes_list,
                COALESCE(
                    (SELECT COUNT(*) FROM codes c 
                     WHERE c.user_id = u.telegram_id AND c.code_type = 'referral'), 0
                ) as referral_count,
                COALESCE(
                    (SELECT COUNT(*) FROM codes c 
                     WHERE c.user_id = u.telegram_id), 0
                ) as total_codes
            FROM users u
            ORDER BY u.created_at DESC
        """)
        return [dict(row) for row in rows]


# =============================================
# 🎟️ CODE OPERATIONS
# =============================================

async def save_code(
    user_id: int,
    code: str,
    code_type: str,
    referred_user_id: Optional[int] = None
) -> dict:
    """💾 Save a new participation code"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO codes (user_id, code, code_type, referred_user_id)
            VALUES ($1, $2, $3, $4)
            RETURNING *
        """, user_id, code, code_type, referred_user_id)
        return dict(row) if row else {}


async def code_exists(code: str) -> bool:
    """🔍 Check if a code already exists in the database"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT 1 FROM codes WHERE code = $1", code
        )
        return row is not None


async def get_user_codes(telegram_id: int) -> List[dict]:
    """📋 Get all codes for a specific user"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT code, code_type, created_at
            FROM codes
            WHERE user_id = $1
            ORDER BY created_at
        """, telegram_id)
        return [dict(row) for row in rows]


async def get_user_code_count(telegram_id: int) -> int:
    """📊 Count total codes for a user"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT COUNT(*) as cnt FROM codes WHERE user_id = $1", telegram_id
        )
        return row["cnt"] if row else 0


async def get_referral_count(telegram_id: int) -> int:
    """🔗 Count referral codes for a user"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT COUNT(*) as cnt FROM codes WHERE user_id = $1 AND code_type = 'referral'",
            telegram_id
        )
        return row["cnt"] if row else 0


# =============================================
# 🏆 LEADERBOARD
# =============================================

async def get_top_referrers(limit: int = 10) -> List[dict]:
    """🏆 Get top referrers leaderboard"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT 
                u.telegram_id,
                u.first_name,
                u.last_name,
                u.username,
                COUNT(c.id) as referral_count
            FROM users u
            JOIN codes c ON c.user_id = u.telegram_id AND c.code_type = 'referral'
            GROUP BY u.telegram_id, u.first_name, u.last_name, u.username
            ORDER BY referral_count DESC
            LIMIT $1
        """, limit)
        return [dict(row) for row in rows]


# =============================================
# 📝 BOT TEXTS OPERATIONS
# =============================================

async def get_text(text_key: str, language: str) -> Optional[dict]:
    """📝 Get a bot text by key and language"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT content, image_file_id
            FROM bot_texts
            WHERE text_key = $1 AND language = $2
        """, text_key, language)
        return dict(row) if row else None


async def update_text(text_key: str, language: str, content: str, image_file_id: Optional[str] = None):
    """✏️ Update or insert a bot text"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO bot_texts (text_key, language, content, image_file_id, updated_at)
            VALUES ($1, $2, $3, $4, NOW())
            ON CONFLICT (text_key, language) DO UPDATE SET
                content = $3,
                image_file_id = COALESCE($4, bot_texts.image_file_id),
                updated_at = NOW()
        """, text_key, language, content, image_file_id)


async def get_all_text_keys() -> List[str]:
    """📋 Get all unique text keys"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT DISTINCT text_key FROM bot_texts ORDER BY text_key"
        )
        return [row["text_key"] for row in rows]


async def clear_text_image(text_key: str, language: str):
    """🗑️ Remove image from a bot text"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE bot_texts SET image_file_id = NULL, updated_at = NOW()
            WHERE text_key = $1 AND language = $2
        """, text_key, language)


# =============================================
# 📢 CHANNEL OPERATIONS
# =============================================

async def get_active_channels() -> List[dict]:
    """📢 Get all active channels"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM channels WHERE is_active = TRUE ORDER BY id"
        )
        return [dict(row) for row in rows]


async def update_channel(channel_id: int, **kwargs):
    """✏️ Update a channel's details"""
    pool = await get_pool()
    allowed = ["channel_type", "channel_id", "channel_url", "channel_name", "is_active"]
    updates = []
    values = []
    idx = 1
    for key, val in kwargs.items():
        if key in allowed:
            updates.append(f"{key} = ${idx}")
            values.append(val)
            idx += 1
    if not updates:
        return
    values.append(channel_id)
    async with pool.acquire() as conn:
        await conn.execute(
            f"UPDATE channels SET {', '.join(updates)} WHERE id = ${idx}",
            *values
        )


async def add_channel(channel_type: str, channel_url: str, channel_name: str, channel_id: str = None) -> dict:
    """➕ Add a new channel"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO channels (channel_type, channel_id, channel_url, channel_name, is_active)
            VALUES ($1, $2, $3, $4, TRUE)
            RETURNING *
        """, channel_type, channel_id, channel_url, channel_name)
        return dict(row) if row else {}


async def remove_channel(channel_db_id: int):
    """🗑️ Remove a channel by its database ID"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM channels WHERE id = $1", channel_db_id)


async def toggle_channel(channel_db_id: int) -> bool:
    """🔄 Toggle channel active/inactive, returns new state"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            UPDATE channels SET is_active = NOT is_active
            WHERE id = $1 RETURNING is_active
        """, channel_db_id)
        return row["is_active"] if row else False


async def get_channel_by_id(channel_db_id: int) -> Optional[dict]:
    """🔍 Get a channel by its database ID"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM channels WHERE id = $1", channel_db_id)
        return dict(row) if row else None


async def get_all_channels() -> List[dict]:
    """📢 Get ALL channels (active and inactive)"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM channels ORDER BY id")
        return [dict(row) for row in rows]


# =============================================
# 📊 STATISTICS
# =============================================

async def get_statistics() -> dict:
    """📊 Get comprehensive bot statistics"""
    pool = await get_pool()
    # 🕐 Today in Tashkent timezone (UTC+5)
    tashkent_tz = timezone(timedelta(hours=5))
    now = datetime.now(tashkent_tz)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    async with pool.acquire() as conn:
        # 📊 Total users
        total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
        # 📊 Today's users
        today_users = await conn.fetchval(
            "SELECT COUNT(*) FROM users WHERE created_at >= $1", today_start
        )
        # 📊 Verified users
        verified_users = await conn.fetchval(
            "SELECT COUNT(*) FROM users WHERE is_verified = TRUE"
        )
        # 📊 Today's verified
        today_verified = await conn.fetchval(
            "SELECT COUNT(*) FROM users WHERE is_verified = TRUE AND created_at >= $1",
            today_start
        )
        # 📊 Total codes
        total_codes = await conn.fetchval("SELECT COUNT(*) FROM codes")
        # 📊 Today's codes
        today_codes = await conn.fetchval(
            "SELECT COUNT(*) FROM codes WHERE created_at >= $1", today_start
        )
        # 📊 Subscription codes
        sub_codes = await conn.fetchval(
            "SELECT COUNT(*) FROM codes WHERE code_type = 'subscription'"
        )
        # 📊 Referral codes
        ref_codes = await conn.fetchval(
            "SELECT COUNT(*) FROM codes WHERE code_type = 'referral'"
        )
        # 📊 Today's referral codes
        today_ref_codes = await conn.fetchval(
            "SELECT COUNT(*) FROM codes WHERE code_type = 'referral' AND created_at >= $1",
            today_start
        )

    return {
        "total_users": total_users or 0,
        "today_users": today_users or 0,
        "verified_users": verified_users or 0,
        "today_verified": today_verified or 0,
        "total_codes": total_codes or 0,
        "today_codes": today_codes or 0,
        "subscription_codes": sub_codes or 0,
        "referral_codes": ref_codes or 0,
        "today_referral_codes": today_ref_codes or 0,
    }
