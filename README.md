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

Final Steps to fix the bot:

   1. Redeploy to Vercel: Run the vercel command or push your changes to
      Vercel.
   2. Get your Vercel URL: It will look like
      https://project-name.vercel.app.
   3. Set the Webhook: Run this command in your terminal (replace YOUR_TOKEN
      and YOUR_VERCEL_URL):

   ###5
   ```bash
"https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://YOUR_VER
     CEL_URL/webhook"
```
```bash
https://api.telegram.org/bot8206647669:AAHUiqdvpWLfwwrIzLw9jExZ6roN6oHqGSQ/setWebhook?url=https://project-geminin.vercel.app//webhook
```

  Once you do this, Telegram will send every message directly to your Vercel
  app, and the bot will respond instantly!

  Summary of fixes:
   - Added a /webhook route in web/app.py.
   - Added a process_update function in bot.py to handle serverless
     requests.
   - Updated utils.py to use /tmp/ for the database on Vercel.

  Your bot should now work perfectly on Vercel!