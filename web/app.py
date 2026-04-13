from flask import Flask, render_template
import sys
import os

# Add parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_leaderboard, get_shop_items, init_db

app = Flask(__name__)

@app.route('/')
def index():
    init_db()
    leaderboard_data = get_leaderboard()
    shop_data = get_shop_items()
    return render_template('index.html', leaderboard=leaderboard_data, shop=shop_data)

if __name__ == '__main__':
    app.run(debug=True)
