#!/usr/bin/env python3
"""
Test run: Post 3 tweets then stop to verify everything works.
"""

import os
import sys
from dotenv import load_dotenv

# Import from the file directly
sys.path.insert(0, os.path.dirname(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location("bot", "solana-hype-bot.py")
bot_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot_module)
NovaStaqTwitterBot = bot_module.NovaStaqTwitterBot

load_dotenv()

if __name__ == "__main__":
    print("=" * 60)
    print("TEST RUN - POSTING 3 TWEETS")
    print("=" * 60)

    bot = NovaStaqTwitterBot()

    for i in range(3):
        print(f"\n[TWEET {i+1}/3]")
        print("-" * 60)

        tweet = bot.generate_unique_tweet()
        if tweet:
            if bot.post_tweet(tweet):
                print(f"[SUCCESS] Tweet {i+1} posted")
            else:
                print(f"[FAILED] Tweet {i+1} failed to post")
        else:
            print(f"[FAILED] Could not generate tweet {i+1}")

    print("\n" + "=" * 60)
    print("[COMPLETE] Test run finished")
    print("=" * 60)
    print(f"\n[TOTAL] Posted {bot.tweets_today} tweets")
    print("\nBot is working! Run with: venv/bin/python solana-hype-bot.py")
