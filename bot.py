import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from utils import init_db, update_user_points, get_leaderboard, get_shop_items, check_winner

# Bot Token (from environment variable)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    init_db()
    update_user_points(user.id, user.username or user.first_name, 0)
    await update.message.reply_text(f"Hello {user.first_name}! Welcome to SuperGameBot.\nUse /xo to play or /shop to see items.")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = get_leaderboard()
    text = "🏆 Leaderboard:\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. {row[0]}: {row[1]} pts\n"
    await update.message.reply_text(text)

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = get_shop_items()
    text = "🛒 Shop:\n"
    for item in items:
        text += f"ID {item[0]}: {item[1]} - {item[2]} pts\n"
    await update.message.reply_text(text)

async def xo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Initialize an empty XO board
    board = ['' for _ in range(9)]
    context.user_data['board'] = board
    keyboard = build_keyboard(board)
    await update.message.reply_text("Let's play XO! Your turn (X).", reply_markup=keyboard)

def build_keyboard(board):
    buttons = []
    for i in range(0, 9, 3):
        buttons.append([
            InlineKeyboardButton(board[i] if board[i] else ' ', callback_data=str(i)),
            InlineKeyboardButton(board[i+1] if board[i+1] else ' ', callback_data=str(i+1)),
            InlineKeyboardButton(board[i+2] if board[i+2] else ' ', callback_data=str(i+2)),
        ])
    return InlineKeyboardMarkup(buttons)

async def handle_xo_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    index = int(query.data)
    board = context.user_data.get('board')
    
    if not board or board[index] != '':
        return

    # Player move (X)
    board[index] = 'X'
    winner = check_winner(board)
    if winner:
        await finish_game(query, board, winner)
        return

    # Bot move (O) - simple random move
    import random
    empty_indices = [i for i, x in enumerate(board) if x == '']
    if empty_indices:
        bot_move = random.choice(empty_indices)
        board[bot_move] = 'O'
        winner = check_winner(board)
        if winner:
            await finish_game(query, board, winner)
            return

    keyboard = build_keyboard(board)
    await query.edit_message_text("Your turn (X).", reply_markup=keyboard)

async def finish_game(query, board, winner):
    keyboard = build_keyboard(board)
    msg = f"Game over! Winner: {winner}"
    if winner == 'X':
        update_user_points(query.from_user.id, query.from_user.username or query.from_user.first_name, 10)
        msg += " (+10 pts!)"
    await query.edit_message_text(msg, reply_markup=keyboard)

async def process_update(json_data):
    if not TOKEN:
        return
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Re-register all handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("xo", xo))
    app.add_handler(CallbackQueryHandler(handle_xo_move))

    # Process the update
    update = Update.de_json(json_data, app.bot)
    
    # Use the app's internal processing logic (requires async context)
    async with app:
        await app.process_update(update)

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
    else:
        init_db()
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("leaderboard", leaderboard))
        app.add_handler(CommandHandler("shop", shop))
        app.add_handler(CommandHandler("xo", xo))
        app.add_handler(CallbackQueryHandler(handle_xo_move))
        app.run_polling()
