import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.app import app

# Export the Flask app as 'app' for Vercel
# Vercel's python runtime expects the variable name to be 'app' by default or configured in vercel.json
# We'll stick to 'app'
