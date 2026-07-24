import os
import threading
from dotenv import load_dotenv
from flask import Flask
import bot  # Import bot.py

load_dotenv()

app = Flask(__name__)

@app.route('/ping')
def ping():
    return "I'm alive!", 200

@app.route('/')
def home():
    return "Birthday Bot is running!", 200

# Chạy Flask server
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Chạy Discord Bot
def run_bot():
    import bot
    bot.run_bot()

if __name__ == "__main__":
    # Chạy Flask trong thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Chạy bot
    run_bot()