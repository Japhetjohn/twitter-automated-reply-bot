#!/usr/bin/env python3
"""
Test Twitter API Credentials
Quick script to verify your API credentials work
"""

import tweepy
import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()

API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

print("=" * 60)
print("Twitter API Credentials Test")
print("=" * 60)
print()

# Check if credentials exist
print("1️⃣ Checking credentials...")
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    print("❌ ERROR: Missing credentials in .env file!")
    exit(1)

print(f"   API Key: {API_KEY[:10]}...")
print(f"   API Secret: {API_SECRET[:10]}...")
print(f"   Access Token: {ACCESS_TOKEN[:10]}...")
print(f"   Access Token Secret: {ACCESS_TOKEN_SECRET[:10]}...")
print("   ✅ All credentials found")
print()

# Test authentication
print("2️⃣ Testing authentication...")
try:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Verify credentials
    user = api.verify_credentials()

    print(f"   ✅ Authentication successful!")
    print()
    print("=" * 60)
    print("Account Information:")
    print("=" * 60)
    print(f"   Username: @{user.screen_name}")
    print(f"   Name: {user.name}")
    print(f"   Followers: {user.followers_count}")
    print(f"   Following: {user.friends_count}")
    print(f"   Tweets: {user.statuses_count}")
    print("=" * 60)
    print()
    print("✅ CREDENTIALS ARE VALID!")
    print("✅ You're ready to run the bot!")
    print()
    print("Next steps:")
    print("  1. Edit twitter-bot.py and customize SEARCH_KEYWORDS")
    print("  2. Edit REPLY_TEMPLATES to match your style")
    print("  3. Run: python twitter-bot.py")
    print()

except tweepy.Unauthorized:
    print("   ❌ Authentication failed!")
    print()
    print("Possible issues:")
    print("  - API keys are incorrect")
    print("  - Access tokens don't match the API keys")
    print("  - App permissions not set correctly")
    print()
    print("Solutions:")
    print("  1. Regenerate your keys at https://developer.twitter.com")
    print("  2. Make sure App permissions are set to 'Read and Write'")
    print("  3. Update .env with new credentials")

except Exception as e:
    print(f"   ❌ Error: {e}")
    print()
    print("Check your internet connection and try again")

print()
