#!/usr/bin/env python3
import tweepy
import time
import random
import os
import json
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import Grok components
from grok_client import GrokClient
from knowledge_base import NovaStaqKnowledgeBase
from prompt_builder import PromptBuilder

load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Hugging Face API configuration (FREE!)
HF_TOKEN = os.getenv('HF_TOKEN')
HF_MODEL = os.getenv('HF_MODEL', 'meta-llama/Llama-3.3-70B-Instruct')
HF_TEMPERATURE = float(os.getenv('HF_TEMPERATURE', '0.7'))
HF_MAX_TOKENS = int(os.getenv('HF_MAX_TOKENS', '150'))

TWEETS_PER_DAY = random.randint(3, 5)
TWEET_HISTORY_FILE = 'tweet_history.json'
MAX_HISTORY = 1000

# Old template arrays removed - now using Grok AI with Novastaq knowledge base
# Fallback templates kept in _generate_fallback_tweet() method

class NovaStaqTwitterBot:
    def __init__(self):
        # Initialize Twitter client
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
        print(f"[OK] @{self.username} - Novastaq AI Bot\n")

        # Initialize Hugging Face AI components
        print("Initializing Hugging Face AI system...")
        self.grok_client = GrokClient(
            api_key=HF_TOKEN,
            model=HF_MODEL,
            temperature=HF_TEMPERATURE,
            max_tokens=HF_MAX_TOKENS
        )
        self.knowledge_base = NovaStaqKnowledgeBase()
        self.prompt_builder = PromptBuilder(self.knowledge_base)
        print("[OK] Hugging Face AI initialized\n")

        # Tweet tracking
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

    def generate_unique_tweet(self, max_attempts=10):
        """
        Generate unique tweet using Grok API with Novastaq knowledge base.

        Returns:
            str: Generated tweet text
        """
        for attempt in range(max_attempts):
            try:
                # 1. Randomly select tweet parameters
                category = self.knowledge_base.get_random_category()
                # More variety: very_short, short, medium, long, very_long
                length_type = random.choice(['very_short', 'short', 'medium', 'long', 'very_long'])

                # 25% chance to focus on specific product
                product = None
                if category['name'] == 'product_spotlight' or random.random() < 0.25:
                    product = self.knowledge_base.get_random_product()

                # 2. Build prompts
                system_prompt = self.prompt_builder.build_system_prompt()
                user_prompt = self.prompt_builder.build_user_prompt(
                    category=category,
                    length_type=length_type,
                    product=product
                )

                # 3. Generate tweet via Grok API
                print(f"[AI] Generating: {category['name']} ({length_type})", end="")
                if product:
                    print(f" - {product['name']}")
                else:
                    print()

                tweet = self.grok_client.generate_tweet(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )

                # 4. Clean and validate
                tweet = self._clean_tweet(tweet)

                # 5. Check uniqueness and length
                if tweet and tweet not in self.history and 50 <= len(tweet) <= 280:
                    print(f"[OK] Generated ({len(tweet)} chars)")
                    return tweet
                else:
                    if tweet in self.history:
                        print(f"[WARN] Duplicate detected, retrying... ({attempt+1}/{max_attempts})")
                    elif tweet:
                        print(f"[WARN] Invalid length ({len(tweet)} chars), retrying...")

            except Exception as e:
                print(f"[ERROR] API error (attempt {attempt+1}): {e}")

                # Try simpler prompt on later attempts
                if attempt >= max_attempts // 2:
                    print("[INFO] Trying simpler prompt...")
                    try:
                        system_prompt, user_prompt = self.prompt_builder.build_simple_fallback_prompt()
                        tweet = self.grok_client.generate_tweet(system_prompt, user_prompt)
                        tweet = self._clean_tweet(tweet)
                        if tweet and tweet not in self.history and 50 <= len(tweet) <= 280:
                            return tweet
                    except:
                        pass

        # Ultimate fallback
        print("[WARN] Max attempts reached, using fallback")
        return self._generate_fallback_tweet()

    def _clean_tweet(self, tweet):
        """
        Clean API output: remove quotes, excess whitespace, emojis.

        Args:
            tweet: Raw tweet from API

        Returns:
            str: Cleaned tweet
        """
        if not tweet:
            return ""

        # Remove surrounding quotes
        tweet = tweet.strip('"\'')

        # Remove emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002700-\U000027BF"  # dingbats
            u"\U0001F900-\U0001F9FF"  # supplemental symbols
            "]+", flags=re.UNICODE)
        tweet = emoji_pattern.sub('', tweet)

        # Remove bullet points and dashes at start of lines
        tweet = re.sub(r'^[-•]\s*', '', tweet, flags=re.MULTILINE)

        # Normalize whitespace
        tweet = ' '.join(tweet.split())

        return tweet.strip()

    def _generate_fallback_tweet(self):
        """
        Simple fallback when Grok API fails.

        Returns:
            str: Simple Novastaq-branded tweet
        """
        products = ["Velcro", "BitNova", "Stakepadi", "Tsara", "Criptpay"]
        topics = [
            "Building decentralized payment infrastructure for Africa.",
            "Bringing Web3 innovation to real-world financial challenges.",
            "The future of payments is decentralized, transparent, and accessible.",
            "Solving liquidity challenges with blockchain technology.",
            "Web3 infrastructure for African payment systems.",
            "Blockchain technology solving real payment problems in Africa.",
            "Decentralized finance meets real-world utility.",
            "Building the payment rails Africa needs."
        ]

        # Try simple format first
        fallback = f"Novastaq: {random.choice(topics)}"
        if fallback not in self.history and len(fallback) <= 280:
            return fallback

        # Try product mention
        fallback = f"{random.choice(products)} is transforming payments in Africa."
        if fallback not in self.history and len(fallback) <= 280:
            return fallback

        # Last resort
        return "Building the future of decentralized payments in Africa."

    def post_tweet(self, text):
        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            self.history.add(text)
            self.save_history()
            self.tweets_today += 1
            print(f"[POSTED] {text}")
            print(f"[URL] https://twitter.com/{self.username}/status/{tweet_id}")
            print(f"[STATS] Today: {self.tweets_today}/{TWEETS_PER_DAY}\n")
            return True
        except Exception as e:
            print(f"[ERROR] {e}")
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
        global TWEETS_PER_DAY
        print("=" * 60)
        print("NOVASTAQ AI TWITTER BOT")
        print("=" * 60)
        print(f"[TARGET] {TWEETS_PER_DAY} tweets/day")
        print(f"[ENGINE] Powered by Hugging Face AI (FREE)")
        print(f"[FOCUS] Novastaq + Web3 Education\n")

        while True:
            try:
                current_date = datetime.now().date()
                if current_date != self.last_tweet_date:
                    print(f"\n[NEW DAY] Yesterday: {self.tweets_today} tweets")
                    self.tweets_today = 0
                    self.last_tweet_date = current_date
                    TWEETS_PER_DAY = random.randint(3, 5)
                    print(f"[TARGET] Today: {TWEETS_PER_DAY} tweets\n")

                if self.tweets_today >= TWEETS_PER_DAY:
                    print(f"[COMPLETE] Goal reached ({self.tweets_today} tweets)")
                    print("[SLEEP] Waiting until tomorrow...")
                    time.sleep(3600)
                    continue

                tweet = self.generate_unique_tweet()
                if self.post_tweet(tweet):
                    wait_seconds = self.calculate_next_tweet_time()
                    next_time = datetime.now() + timedelta(seconds=wait_seconds)
                    print(f"[NEXT] {next_time.strftime('%I:%M %p')}")
                    time.sleep(wait_seconds)
                else:
                    time.sleep(1800)

            except KeyboardInterrupt:
                print(f"\n[STOPPED] Today: {self.tweets_today} tweets")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(600)

if __name__ == "__main__":
    # Validate credentials
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
        print("[ERROR] Missing Twitter API credentials!")
        exit(1)

    if not HF_TOKEN or HF_TOKEN == "YOUR_HF_TOKEN_HERE":
        print("[ERROR] Missing Hugging Face API token!")
        print("[INFO] Get your free token at: https://huggingface.co/settings/tokens")
        exit(1)

    # Start bot
    bot = NovaStaqTwitterBot()
    bot.run()
