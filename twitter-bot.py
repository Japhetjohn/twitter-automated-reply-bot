#!/usr/bin/env python3
"""
Twitter Bot for Blockchain Developers (Free Tier - API v2)
- Auto-replies to crypto/web3/blockchain tweets
- Retweets relevant content
- Optimized for FREE TIER: 50 tweets/month limit
- Uses Twitter API v2 (free tier compatible)
"""

import tweepy
import time
import random
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============== TWITTER API CREDENTIALS ==============
# For v2 API, we need Bearer Token for read operations
# and OAuth 1.0a for write operations (replies, retweets)
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# ============== BLOCKCHAIN/WEB3/CRYPTO KEYWORDS ==============
# Massive list of keywords to search and engage with
SEARCH_KEYWORDS = [
    # Major Blockchains
    "ethereum",
    "solana",
    "bitcoin",
    "cardano",
    "polygon",
    "avalanche",
    "polkadot",
    "cosmos",
    "near protocol",
    "sui blockchain",
    "aptos",

    # Web3 & Blockchain General
    "web3",
    "blockchain",
    "crypto",
    "cryptocurrency",
    "DeFi",
    "smart contracts",
    "dapps",
    "web3 dev",

    # NFTs & Gaming
    "NFT",
    "web3 gaming",
    "GameFi",

    # Programming (no hashtags for better results)
    "solidity",
    "rust programming",
    "blockchain development",

    # DeFi Protocols
    "uniswap",
    "aave",
    "compound finance",

    # Developer Topics
    "smart contract development",
    "blockchain developer",
    "web3 developer",
    "gas optimization",

    # Crypto Culture
    "buidl",
    "gm crypto",
    "WAGMI",

    # Layer 2s
    "arbitrum",
    "optimism",
    "zksync",

    # Other Topics
    "DAO",
    "tokenomics",
]

# ============== REPLY TEMPLATES ==============
# Engaging, natural replies for blockchain/crypto content
REPLY_TEMPLATES = [
    # Developer appreciation
    "This is actually a solid approach 🔥",
    "Been working on something similar, great minds think alike 💡",
    "The code implementation here is clean ✨",
    "Love seeing more devs building in web3 🔨",
    "This is the way 🎯",
    "Really well explained bro 💯",
    "Great breakdown 🏗️",
    "This optimization is genius ⚡",
    "Love the gas efficiency approach 💰",
    "Smart contract design on point 🎨",
    "This thread is gold 🌟",

    # Crypto/Blockchain specific
    "Bullish on this tech 🚀",
    "This is going to change the game 🎮",
    "Finally someone gets it 🧠",
    "We're still early ⏰",
    "WAGMI 💪",
    "Facts! 📊",
    "This right here 👆",
    "Based take 🗿",
    "LFG! 🔥",
    "Couldn't agree more 🤝",

    # General engagement
    "Facts bro 💯",
    "This 🔥",
    "100% agree ✅",
    "Real talk 💬",
    "Exactly what I've been saying 👏",
    "This needs more visibility 📢",
    "Great point 🎯",
    "Well said 🗣️",
    "Truth 💎",
    "Absolutely 🙌",

    # Technical responses
    "Have you tried optimizing the gas costs? 💡",
    "The security implications here are interesting 🔐",
    "This pattern works well for scalability 📈",
    "Great use case 🎯",
]

# ============== FREE TIER RATE LIMITS ==============
# Free tier: 50 tweets/month write limit
MIN_DELAY = 300  # 5 minutes between actions
MAX_DELAY = 900  # 15 minutes between actions
ACTIONS_PER_DAY = 2  # Only 2 actions per day
MAX_ACTIONS_PER_MONTH = 45  # Stop at 45 to stay under 50

# Action probabilities (NO ORIGINAL TWEETS)
REPLY_PROBABILITY = 0.70  # 70% replies
RETWEET_PROBABILITY = 0.30  # 30% retweets

SELECTION_RATE = 0.3  # Act on 30% of found tweets

# ============== BOT CLASS ==============

class TwitterBot:
    def __init__(self):
        """Initialize Twitter API v2 client"""
        try:
            # Create v2 client with both read (bearer) and write (OAuth) capabilities
            self.client = tweepy.Client(
                bearer_token=BEARER_TOKEN,
                consumer_key=API_KEY,
                consumer_secret=API_SECRET,
                access_token=ACCESS_TOKEN,
                access_token_secret=ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )

            # Get our own user info
            me = self.client.get_me()
            self.my_id = me.data.id
            self.my_username = me.data.username

            print(f"[{self.timestamp()}] ✅ Authentication successful!")
            print(f"[{self.timestamp()}] 🤖 @{self.my_username} - Blockchain Dev Bot")
            print(f"[{self.timestamp()}] 🎯 FREE TIER MODE: Max {ACTIONS_PER_DAY} actions/day")
            print(f"[{self.timestamp()}] 📋 70% replies, 30% retweets\n")

            # Track processed tweets
            self.processed_tweets = set()

            # Track daily and monthly actions
            self.daily_actions = 0
            self.monthly_actions = 0
            self.last_action_date = datetime.now().date()

        except Exception as e:
            print(f"❌ Error during authentication: {e}")
            exit(1)

    def timestamp(self):
        """Get current timestamp string"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def random_delay(self):
        """Generate random delay between actions"""
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        minutes = delay // 60
        print(f"[{self.timestamp()}] ⏳ Waiting {minutes} minutes ({delay}s)...")
        time.sleep(delay)

    def check_daily_limit(self):
        """Check if we've hit daily action limit"""
        current_date = datetime.now().date()

        # Reset daily counter if new day
        if current_date != self.last_action_date:
            print(f"[{self.timestamp()}] 📅 New day! Resetting daily counter.")
            print(f"[{self.timestamp()}] 📊 Yesterday's actions: {self.daily_actions}")
            self.daily_actions = 0
            self.last_action_date = current_date

        # Check daily limit
        if self.daily_actions >= ACTIONS_PER_DAY:
            return False

        # Check monthly limit
        if self.monthly_actions >= MAX_ACTIONS_PER_MONTH:
            print(f"[{self.timestamp()}] 🛑 MONTHLY LIMIT REACHED ({MAX_ACTIONS_PER_MONTH} actions)")
            print(f"[{self.timestamp()}] 🛑 Stopping to avoid exceeding free tier!")
            return False

        return True

    def generate_reply(self):
        """Generate a random reply"""
        return random.choice(REPLY_TEMPLATES)

    def search_tweets(self):
        """Search for tweets using v2 API"""
        try:
            # Pick random keyword
            keyword = random.choice(SEARCH_KEYWORDS)
            print(f"[{self.timestamp()}] 🔍 Searching for: {keyword}")

            # Search using v2 API (free tier has access to this)
            # Note: Free tier has limited search, only gets tweets from last 7 days
            response = self.client.search_recent_tweets(
                query=f"{keyword} -is:retweet -is:reply lang:en",
                max_results=10,
                tweet_fields=['author_id', 'created_at', 'text']
            )

            if not response.data:
                print(f"[{self.timestamp()}] 📊 Found 0 new tweets")
                return []

            # Filter out already processed tweets and our own tweets
            new_tweets = [
                t for t in response.data
                if t.id not in self.processed_tweets
                and str(t.author_id) != str(self.my_id)
            ]

            print(f"[{self.timestamp()}] 📊 Found {len(new_tweets)} new tweets")
            return new_tweets

        except Exception as e:
            print(f"[{self.timestamp()}] ❌ Error searching tweets: {e}")
            return []

    def should_act_on_tweet(self):
        """Decide whether to act on a tweet"""
        return random.random() < SELECTION_RATE

    def reply_to_tweet(self, tweet):
        """Reply to a tweet using v2 API"""
        try:
            reply_text = self.generate_reply()

            # Get tweet preview
            tweet_preview = tweet.text[:50] + "..." if len(tweet.text) > 50 else tweet.text

            # Post reply using v2 API
            response = self.client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet.id
            )

            print(f"[{self.timestamp()}] 💬 REPLIED: '{reply_text}'")
            print(f"[{self.timestamp()}]    Tweet ID: {tweet.id}")
            print(f"[{self.timestamp()}]    Original: \"{tweet_preview}\"")

            self.processed_tweets.add(tweet.id)
            self.daily_actions += 1
            self.monthly_actions += 1

            return True

        except tweepy.TweepyException as e:
            print(f"[{self.timestamp()}] ❌ Error replying: {e}")
            return False

    def retweet_tweet(self, tweet):
        """Retweet a tweet using v2 API"""
        try:
            # Get tweet preview
            tweet_preview = tweet.text[:50] + "..." if len(tweet.text) > 50 else tweet.text

            # Retweet using v2 API
            self.client.retweet(tweet.id)

            print(f"[{self.timestamp()}] 🔄 RETWEETED")
            print(f"[{self.timestamp()}]    Tweet ID: {tweet.id}")
            print(f"[{self.timestamp()}]    Original: \"{tweet_preview}\"")

            self.processed_tweets.add(tweet.id)
            self.daily_actions += 1
            self.monthly_actions += 1

            return True

        except tweepy.TweepyException as e:
            print(f"[{self.timestamp()}] ❌ Error retweeting: {e}")
            return False

    def process_tweet(self, tweet):
        """Decide whether to reply or retweet"""
        # Skip if we shouldn't act on this tweet
        if not self.should_act_on_tweet():
            return False

        # Decide action: reply or retweet
        if random.random() < REPLY_PROBABILITY:
            return self.reply_to_tweet(tweet)
        else:
            return self.retweet_tweet(tweet)

    def run(self):
        """Main bot loop"""
        print(f"[{self.timestamp()}] 🚀 Bot starting...")
        print(f"[{self.timestamp()}] 📊 Monthly: {self.monthly_actions}/{MAX_ACTIONS_PER_MONTH}")
        print(f"[{self.timestamp()}] 📊 Daily: {self.daily_actions}/{ACTIONS_PER_DAY}\n")

        while True:
            try:
                # Check if we can still perform actions
                if not self.check_daily_limit():
                    if self.monthly_actions >= MAX_ACTIONS_PER_MONTH:
                        print(f"[{self.timestamp()}] 🛑 Monthly limit reached. Exiting...")
                        break
                    else:
                        # Daily limit reached
                        print(f"[{self.timestamp()}] 😴 Daily limit reached")
                        print(f"[{self.timestamp()}] 💤 Sleeping for 1 hour...")
                        time.sleep(3600)
                        continue

                # Search for tweets
                tweets = self.search_tweets()

                if not tweets:
                    print(f"[{self.timestamp()}] 💤 No tweets found, waiting...\n")
                    time.sleep(random.randint(60, 180))
                    continue

                # Process tweets
                acted = False
                for tweet in tweets[:5]:
                    if self.process_tweet(tweet):
                        acted = True
                        print(f"[{self.timestamp()}] 📊 Daily: {self.daily_actions}/{ACTIONS_PER_DAY} | Monthly: {self.monthly_actions}/{MAX_ACTIONS_PER_MONTH}\n")

                        # Check limit after action
                        if not self.check_daily_limit():
                            break

                        # Wait before next action
                        self.random_delay()
                        break  # Only one action per search

                if not acted:
                    print(f"[{self.timestamp()}] 💤 No action taken\n")
                    time.sleep(random.randint(60, 180))

            except KeyboardInterrupt:
                print(f"\n[{self.timestamp()}] 🛑 Bot stopped by user")
                print(f"[{self.timestamp()}] 📊 Final stats:")
                print(f"[{self.timestamp()}]    Daily: {self.daily_actions}")
                print(f"[{self.timestamp()}]    Monthly: {self.monthly_actions}")
                break
            except Exception as e:
                print(f"[{self.timestamp()}] ❌ Unexpected error: {e}")
                time.sleep(300)

# ============== MAIN ==============

if __name__ == "__main__":
    print("=" * 60)
    print("🔗 Twitter Bot for Blockchain Developers (FREE TIER)")
    print("=" * 60)
    print()

    # Validate credentials
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
        print("❌ Error: Missing Twitter API credentials!")
        print()
        print("Make sure .env file has all credentials including BEARER_TOKEN")
        exit(1)

    # Start bot
    bot = TwitterBot()
    bot.run()
