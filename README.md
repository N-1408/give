# 🎁 Telegram Giveaway Bot

Telegram giveaway bot with referral system, unique codes, and admin panel.

## Features

- 🌐 Multi-language support (UZ/RU/EN)
- 📢 Channel subscription verification
- 🎟️ Unique participation codes
- 🔗 Referral system with bonus codes
- 📊 Admin panel with statistics
- 📝 Dynamic text management
- 📥 Excel export
- 📢 Broadcast messaging

## Setup

1. Copy `.env.example` to `.env` and fill in your values
2. Install dependencies: `pip install -r requirements.txt`
3. Run SQL schema on Supabase
4. Start bot: `python -m bot.main`

## Deployment (Render)

1. Push to GitHub
2. Create Web Service on Render
3. Set environment variables
4. Deploy

## Tech Stack

- Python 3.11+ / aiogram 3.4
- Supabase (PostgreSQL) via asyncpg
- Render (Web Service)
