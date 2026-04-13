# SuperGameBot

A Telegram bot with games (XO), a shop, and a web dashboard, built with Python (Flask) and SQLite.

## Project Structure
- `bot.py`: Telegram bot using `python-telegram-bot`.
- `web/`: Flask web application for the dashboard.
- `utils.py`: Core logic for database, shop, and games.
- `api/index.py`: Vercel serverless function entry point.
- `vercel.json`: Vercel configuration.

## Setup & Deployment

### 1. Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Locally
1. Set your Telegram bot token:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token_here"
   ```
2. Start the bot:
   ```bash
   python bot.py
   ```
3. Start the dashboard:
   ```bash
   python web/app.py
   ```

### 3. Deploy to Vercel
1. Install [Vercel CLI](https://vercel.com/download).
2. Run `vercel`.
3. Set `TELEGRAM_BOT_TOKEN` in Vercel's environment variables if needed (though the bot usually runs on a persistent server).

### Note on Database Persistence
This project uses **SQLite**. On Vercel (serverless), the database file (`db.sqlite`) will be **reset** periodically. For long-term data persistence, it is recommended to use a remote database like MongoDB or PostgreSQL.
