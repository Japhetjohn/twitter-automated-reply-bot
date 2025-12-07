#!/usr/bin/env python3
"""
Post a single test tweet to verify everything works.
"""

import os
import re
import random
from dotenv import load_dotenv
import tweepy
from grok_client import GrokClient
from knowledge_base import NovaStaqKnowledgeBase
from prompt_builder import PromptBuilder

load_dotenv()

# Twitter credentials
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Hugging Face credentials
HF_TOKEN = os.getenv('HF_TOKEN')
HF_MODEL = os.getenv('HF_MODEL', 'meta-llama/Llama-3.3-70B-Instruct')

def clean_tweet(tweet):
    """Remove emojis and clean tweet."""
    if not tweet:
        return ""

    tweet = tweet.strip('"\'')

    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U0001F900-\U0001F9FF"
        "]+", flags=re.UNICODE)
    tweet = emoji_pattern.sub('', tweet)

    tweet = re.sub(r'^[-•]\s*', '', tweet, flags=re.MULTILINE)
    tweet = ' '.join(tweet.split())

    return tweet.strip()

def main():
    print("=" * 60)
    print("POSTING TEST TWEET")
    print("=" * 60)

    # Initialize components
    print("\n📚 Loading knowledge base...")
    kb = NovaStaqKnowledgeBase()

    print("🤖 Initializing AI...")
    client = GrokClient(api_key=HF_TOKEN, model=HF_MODEL, temperature=0.7, max_tokens=150)
    prompt_builder = PromptBuilder(kb)

    print("🐦 Connecting to Twitter...")
    twitter_client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True
    )

    me = twitter_client.get_me()
    username = me.data.username
    print(f"✅ Connected as @{username}\n")

    # Generate tweet
    print("🎲 Generating tweet...")
    category = kb.get_random_category()
    length_type = random.choice(['short', 'long'])
    product = kb.get_random_product() if random.random() < 0.3 else None

    print(f"   Category: {category['name']}")
    print(f"   Length: {length_type}")
    if product:
        print(f"   Product: {product['name']}")

    system_prompt = prompt_builder.build_system_prompt()
    user_prompt = prompt_builder.build_user_prompt(category, length_type, product)

    tweet = client.generate_tweet(system_prompt, user_prompt)
    tweet = clean_tweet(tweet)

    print(f"\n📝 Generated tweet ({len(tweet)} chars):")
    print(f"   \"{tweet}\"\n")

    # Confirm
    print("🚀 Posting to Twitter...")
    response = twitter_client.create_tweet(text=tweet)
    tweet_id = response.data['id']

    print("\n" + "=" * 60)
    print("✅ TWEET POSTED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n🔗 View it here: https://twitter.com/{username}/status/{tweet_id}")
    print(f"\n📊 Tweet: \"{tweet}\"")
    print(f"\n💡 Category: {category['name']}")
    print(f"📏 Length: {len(tweet)} characters\n")

if __name__ == "__main__":
    main()
