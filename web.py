#!/usr/bin/env python3
"""
Web wrapper for the Solana Hype Bot
Runs the bot in a background thread while serving a simple web interface
"""
import os
import threading
from flask import Flask, jsonify, render_template_string
from datetime import datetime

# Import the bot
import sys
sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)

# Store bot status
bot_status = {
    "status": "starting",
    "started_at": datetime.now().isoformat(),
    "tweets_today": 0,
    "last_tweet": None,
    "error": None
}

# Simple HTML dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Solana Hype Bot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #0f0f23;
            color: #e0e0e0;
        }
        .container {
            background: #1a1a2e;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        h1 {
            color: #9945FF;
            margin-top: 0;
        }
        .status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .status.running {
            background: #14F195;
            color: #000;
        }
        .status.error {
            background: #ff4444;
            color: #fff;
        }
        .stat {
            margin: 15px 0;
            padding: 10px;
            background: #0f0f23;
            border-radius: 8px;
        }
        .stat-label {
            color: #888;
            font-size: 14px;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #14F195;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }
        a {
            color: #9945FF;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    <script>
        function updateStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('status').innerText = data.status;
                    document.getElementById('status').className = 'status ' + data.status;
                    document.getElementById('tweets').innerText = data.tweets_today;
                    document.getElementById('last-tweet').innerText = data.last_tweet || 'None yet';
                    if (data.error) {
                        document.getElementById('error').innerText = 'Error: ' + data.error;
                        document.getElementById('error').style.display = 'block';
                    }
                });
        }
        setInterval(updateStatus, 5000);
        updateStatus();
    </script>
</head>
<body>
    <div class="container">
        <h1>🚀 Solana Hype Bot</h1>
        <p>Status: <span id="status" class="status running">{{ status }}</span></p>

        <div class="stat">
            <div class="stat-label">Tweets Today</div>
            <div class="stat-value" id="tweets">{{ tweets_today }}</div>
        </div>

        <div class="stat">
            <div class="stat-label">Last Tweet</div>
            <div class="stat-value" style="font-size: 16px;" id="last-tweet">{{ last_tweet or 'None yet' }}</div>
        </div>

        <div class="stat">
            <div class="stat-label">Running Since</div>
            <div class="stat-value" style="font-size: 16px;">{{ started_at }}</div>
        </div>

        <div id="error" style="display: none; color: #ff4444; margin-top: 20px;"></div>

        <div class="footer">
            <p>💜 Powered by Solana | 🤖 Running on Render</p>
            <p><a href="/api/status">API Status</a> | <a href="/health">Health Check</a></p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Dashboard"""
    return render_template_string(
        DASHBOARD_HTML,
        status=bot_status['status'],
        tweets_today=bot_status['tweets_today'],
        last_tweet=bot_status['last_tweet'],
        started_at=bot_status['started_at']
    )

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "ok",
        "service": "solana-hype-bot",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status')
def status():
    """Bot status API"""
    return jsonify(bot_status)

def run_bot():
    """Run the bot in a background thread"""
    try:
        bot_status['status'] = 'running'

        # Check credentials
        if not all([
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET'),
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            os.getenv('TWITTER_BEARER_TOKEN')
        ]):
            bot_status['status'] = 'error'
            bot_status['error'] = 'Missing Twitter credentials'
            print("❌ Missing Twitter credentials!")
            return

        # Import the bot using importlib (handles hyphens in filename)
        import importlib.util
        spec = importlib.util.spec_from_file_location("bot", "solana-hype-bot.py")
        bot_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bot_module)

        # Create and run bot
        bot = bot_module.SolanaHypeBot()

        # Monkey-patch the post_tweet method to update status
        original_post_tweet = bot.post_tweet
        def patched_post_tweet(text):
            result = original_post_tweet(text)
            if result:
                bot_status['tweets_today'] = bot.tweets_today
                bot_status['last_tweet'] = text[:100] + '...' if len(text) > 100 else text
            return result
        bot.post_tweet = patched_post_tweet

        bot.run()

    except Exception as e:
        bot_status['status'] = 'error'
        bot_status['error'] = str(e)
        print(f"❌ Bot error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Start Flask web server
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
