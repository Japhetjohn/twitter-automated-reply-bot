#!/usr/bin/env python3
import tweepy
import time
import random
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

TWEETS_PER_DAY = random.randint(3, 5)
TWEET_HISTORY_FILE = 'tweet_history.json'
MAX_HISTORY = 1000

SOLANA_TOPICS = [
    "Solana", "SOL", "$SOL", "@solana", "Solana Network",
    "Solana DeFi", "Solana NFTs", "Solana Speed", "Phantom Wallet",
    "Jupiter", "Marinade", "Drift Protocol", "Kamino", "Marginfi",
    "Jito", "Pyth Network", "Wormhole", "Raydium", "Orca",
    "Solana Mobile", "Saga Phone", "Chapter 2", "Solana Pay",
    "Solana Breakpoint", "Firedancer", "Solana Labs", "Helius",
    "Solana validator", "Solana staking", "liquid staking", "mSOL",
    "Solana MEV", "Solana blinks", "Actions", "compressed NFTs"
]

ENGAGEMENT_HOOKS = [
    "\n\nThoughts?",
    "\n\nAgree?",
    "\n\nAm I wrong?",
    "\n\nWho else sees this?",
    "\n\nLFG",
    "\n\nWAGMI",
    "\n\nChange my mind",
    "\n\nDrop your take",
    "\n\nYour move, Ethereum",
    "\n\nSolana season"
]

HYPE_TEMPLATES = [
    "{topic} is doing {metric} and nobody's talking about it.\n\n{reason}{hook}",
    "{topic} just {achievement}.\n\n{sentiment}{hook}",
    "{topic} will {prediction} by {timeframe}.\n\n{reason}{hook}",
    "Everyone's sleeping on {topic} while {comparison}.{hook}",
    "{topic} {metric}.\n\n{sentiment}\n\nWe're still early.{hook}",
    "The {topic} ecosystem is {sentiment}.\n\n{reason}{hook}",
    "{topic}: {stat}\n\n{comparison}{hook}",
    "Remember when they said {fud}?\n\n{topic} just {achievement}.{hook}",
    "If you're not building on {topic}, you're missing {opportunity}.{hook}",
    "{topic} {fact}.{hook}",
    "{topic} developers are {action} while everyone's {distraction}.{hook}",
    "The {topic} community is different.\n\n{reason}{hook}",
    "{topic} {metric} and we're supposed to stay calm?{hook}",
    "{topic} flipping narratives:\n\n{fud} vs {reality}{hook}",
    "{topic} {hot_take}.{hook}"
]

METRICS = [
    "400ms block times", "processing 65k TPS", "sub-cent fees",
    "growing 300% MoM", "at all-time high TVL", "onboarding millions",
    "hitting new milestones daily", "outpacing all competitors",
    "breaking every record", "doubling every quarter"
]

ACHIEVEMENTS = [
    "processed more transactions than all other L1s combined",
    "onboarded 10M+ new users this month", "hit $8B TVL",
    "achieved 99.99% uptime", "launched the most consumer-friendly wallet",
    "made NFTs actually usable with compression", "solved the MEV problem",
    "shipped Firedancer testnet", "proved scalability is possible"
]

PREDICTIONS = [
    "flip Ethereum in users", "10x from here", "become the iOS of crypto",
    "dominate consumer crypto", "be the default chain for developers",
    "power the next billion users", "win the mobile race"
]

TIMEFRAMES = ["2025", "Q1", "Q2", "this year", "6 months", "next cycle"]

REASONS = [
    "The speed is unmatched", "Developer experience is *chef's kiss*",
    "Real users, real adoption", "The tech just works",
    "Network effects are compounding", "Builders are choosing Solana",
    "Mobile integration is game-changing", "Fees make sense for consumers",
    "The ecosystem is thriving", "Innovation happening daily"
]

COMPARISONS = [
    "other chains are still debating scaling",
    "Ethereum is stuck at 15 TPS", "competitors can't keep up",
    "legacy systems look ancient", "old chains are pivoting",
    "everyone else is talking, Solana is building"
]

STATS = [
    "400ms blocks. Zero compromises.",
    "65,000 TPS. Actually working.",
    "$0.00025 per transaction. Not a typo.",
    "99.99% uptime in 2024. Facts.",
    "3M+ daily active addresses. Real usage."
]

FUD_POINTS = [
    "Solana was dead", "the network would never be stable",
    "high TPS was impossible", "developers were leaving",
    "it was just for degens", "mobile phones were a gimmick"
]

REALITIES = [
    "Processing more txns than ever", "99.99% uptime achieved",
    "Developers can't stop building", "Consumer apps are thriving",
    "Saga sold out, Chapter 2 incoming"
]

OPPORTUNITIES = [
    "the fastest growing ecosystem in crypto",
    "the best developer experience", "actual consumer adoption",
    "real-world use cases", "the mobile revolution"
]

FACTS = [
    "has more daily active users than most L1s combined",
    "processed more transactions than Visa last month",
    "is the only chain that actually scales", "makes other L1s obsolete",
    "is what crypto was supposed to be"
]

ACTIONS = [
    "shipping features", "solving real problems",
    "onboarding normies", "building in silence"
]

DISTRACTIONS = [
    "arguing about rollups", "debating trilemmas",
    "hyping vaporware", "fighting on Twitter"
]

HOT_TAKES = [
    "already won, we're just waiting for everyone to realize",
    "is the only chain that doesn't need L2s because it actually works",
    "will eat Ethereum's lunch by 2025", "is severely undervalued"
]

SENTIMENTS = [
    "This is bullish.", "Game over.", "Not even close.",
    "Absolutely massive.", "The future is here.", "This is the way.",
    "Unmatched.", "Next level.", "Insane.", "Chef's kiss."
]

class SolanaHypeBot:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        me = self.client.get_me()
        self.username = me.data.username
        print(f"✅ @{self.username} - Solana Hype Bot\n")
        self.history = self.load_history()
        self.tweets_today = 0
        self.last_tweet_date = datetime.now().date()

    def load_history(self):
        try:
            with open(TWEET_HISTORY_FILE, 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()

    def save_history(self):
        history_list = list(self.history)[-MAX_HISTORY:]
        with open(TWEET_HISTORY_FILE, 'w') as f:
            json.dump(history_list, f)

    def generate_unique_tweet(self):
        for _ in range(50):
            template = random.choice(HYPE_TEMPLATES)
            tweet = template.format(
                topic=random.choice(SOLANA_TOPICS),
                metric=random.choice(METRICS),
                achievement=random.choice(ACHIEVEMENTS),
                prediction=random.choice(PREDICTIONS),
                timeframe=random.choice(TIMEFRAMES),
                reason=random.choice(REASONS),
                comparison=random.choice(COMPARISONS),
                stat=random.choice(STATS),
                fud=random.choice(FUD_POINTS),
                reality=random.choice(REALITIES),
                opportunity=random.choice(OPPORTUNITIES),
                fact=random.choice(FACTS),
                action=random.choice(ACTIONS),
                distraction=random.choice(DISTRACTIONS),
                hot_take=random.choice(HOT_TAKES),
                sentiment=random.choice(SENTIMENTS),
                hook=random.choice(ENGAGEMENT_HOOKS)
            ).strip()
            tweet = ' '.join(tweet.split())
            if tweet not in self.history and len(tweet) <= 280:
                return tweet
        return f"Solana is {random.choice(SENTIMENTS)}{random.choice(ENGAGEMENT_HOOKS)}"

    def post_tweet(self, text):
        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            self.history.add(text)
            self.save_history()
            self.tweets_today += 1
            print(f"✅ POSTED: {text}")
            print(f"🔗 https://twitter.com/{self.username}/status/{tweet_id}")
            print(f"📊 Today: {self.tweets_today}/{TWEETS_PER_DAY}\n")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def calculate_next_tweet_time(self):
        current_hour = datetime.now().hour
        if current_hour >= 23 or current_hour < 8:
            tomorrow_morning = datetime.now().replace(
                hour=random.randint(8, 10), minute=random.randint(0, 59), second=0
            ) + timedelta(days=1 if current_hour >= 23 else 0)
            return (tomorrow_morning - datetime.now()).total_seconds()
        return random.uniform(2, 6) * 3600

    def run(self):
        print("=" * 60)
        print("🚀 SOLANA HYPE BOT")
        print("=" * 60)
        print(f"📊 Target: {TWEETS_PER_DAY} tweets/day")
        print(f"💜 100% Solana-focused")
        print(f"🎯 Engagement-optimized\n")

        while True:
            try:
                current_date = datetime.now().date()
                if current_date != self.last_tweet_date:
                    print(f"\n📅 New day! Yesterday: {self.tweets_today} tweets")
                    self.tweets_today = 0
                    self.last_tweet_date = current_date
                    global TWEETS_PER_DAY
                    TWEETS_PER_DAY = random.randint(3, 5)
                    print(f"🎯 Today: {TWEETS_PER_DAY} tweets\n")

                if self.tweets_today >= TWEETS_PER_DAY:
                    print(f"✅ Goal reached ({self.tweets_today} tweets)")
                    print("💤 Sleeping until tomorrow...")
                    time.sleep(3600)
                    continue

                tweet = self.generate_unique_tweet()
                if self.post_tweet(tweet):
                    wait_seconds = self.calculate_next_tweet_time()
                    next_time = datetime.now() + timedelta(seconds=wait_seconds)
                    print(f"⏰ Next: {next_time.strftime('%I:%M %p')}")
                    time.sleep(wait_seconds)
                else:
                    time.sleep(1800)

            except KeyboardInterrupt:
                print(f"\n🛑 Stopped. Today: {self.tweets_today} tweets")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(600)

if __name__ == "__main__":
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
        print("❌ Missing credentials!")
        exit(1)
    bot = SolanaHypeBot()
    bot.run()
