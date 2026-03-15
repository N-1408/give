# ============================================
# 🎟️ Code Generator Module - Telegram Giveaway Bot
# 📁 File: bot/code_generator.py
# 👤 Created by: User with AI
# 📝 Generates unique 6-character alphanumeric participation codes.
#    Uses a safe charset excluding confusing characters (0/O, 1/I/L).
#    Includes collision detection with retry mechanism for safety.
# 📅 Created: 2026-03-15 07:47 (Tashkent Time)
# ============================================

import random
import string
import logging
from bot import database as db

logger = logging.getLogger(__name__)

# 🔤 Safe character set (excluding confusing chars: 0/O, 1/I/L)
# Total: 30 characters → 30^6 = 729,000,000 possible codes ✅
SAFE_CHARS = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

# 📏 Code length
CODE_LENGTH = 6

# 🔄 Max retry attempts for collision
MAX_RETRIES = 10


def _generate_raw_code() -> str:
    """🎲 Generate a random 6-character code from safe charset"""
    return "".join(random.choices(SAFE_CHARS, k=CODE_LENGTH))


async def generate_unique_code() -> str:
    """
    🎟️ Generate a unique participation code

    Generates a 6-char alphanumeric code and verifies it doesn't
    exist in the database. Retries up to MAX_RETRIES times on collision.

    Returns:
        str: A unique 6-character code (e.g. 'A3K9X2')

    Raises:
        RuntimeError: If unable to generate unique code after retries
    """
    for attempt in range(MAX_RETRIES):
        code = _generate_raw_code()

        # 🔍 Check uniqueness in database
        if not await db.code_exists(code):
            logger.debug(f"✅ Generated unique code: {code} (attempt {attempt + 1})")
            return code

        logger.warning(f"⚠️ Code collision: {code}, retrying... (attempt {attempt + 1})")

    # ❌ Extremely unlikely with 729M possible codes
    raise RuntimeError(
        f"Failed to generate unique code after {MAX_RETRIES} attempts. "
        "This should not happen with the current charset and code length."
    )
