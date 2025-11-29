#!/bin/bash
# Quick start script for Twitter bot (Free Tier Optimized)

cd "$(dirname "$0")"

echo "============================================================"
echo "🔗 Twitter Bot for Blockchain Developers (FREE TIER)"
echo "Account: @gracejaphet_"
echo "============================================================"
echo ""

# Activate virtual environment
source venv/bin/activate

# Run the bot
python twitter-bot.py
