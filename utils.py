import sqlite3

def init_db():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT, points INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shop
                 (item_id INTEGER PRIMARY KEY, name TEXT, price INTEGER)''')
    # Add some initial shop items
    c.execute("INSERT OR IGNORE INTO shop (item_id, name, price) VALUES (1, 'Premium Badge', 100)")
    c.execute("INSERT OR IGNORE INTO shop (item_id, name, price) VALUES (2, 'Game Pass', 500)")
    conn.commit()
    conn.close()

def get_user_points(user_id):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def update_user_points(user_id, username, points):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, points) VALUES (?, ?, 0)", (user_id, username))
    c.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("SELECT username, points FROM users ORDER BY points DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return rows

def get_shop_items():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("SELECT * FROM shop")
    rows = c.fetchall()
    conn.close()
    return rows

# XO Game logic (simplified)
def check_winner(board):
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != '':
            return board[line[0]]
    if '' not in board:
        return 'Tie'
    return None
