#!/usr/bin/env python3
"""
Test script for Grok API integration.
Tests connectivity and generates sample tweets without posting.
"""

import os
from dotenv import load_dotenv
from grok_client import GrokClient
from knowledge_base import NovaStaqKnowledgeBase
from prompt_builder import PromptBuilder
import random

load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')
HF_MODEL = os.getenv('HF_MODEL', 'meta-llama/Llama-3.3-70B-Instruct')

def test_grok_connection():
    """Test Hugging Face API connectivity."""
    print("=" * 60)
    print("TESTING HUGGING FACE API CONNECTION")
    print("=" * 60)

    client = GrokClient(api_key=HF_TOKEN, model=HF_MODEL)
    success = client.test_connection()

    if success:
        print("\n✅ Hugging Face API is working!\n")
        return True
    else:
        print("\n❌ Hugging Face API connection failed!\n")
        return False

def test_knowledge_base():
    """Test knowledge base loading."""
    print("=" * 60)
    print("TESTING KNOWLEDGE BASE")
    print("=" * 60)

    kb = NovaStaqKnowledgeBase()

    print(f"\n📊 Statistics:")
    print(f"   Products: {len(kb.get_all_products())}")
    print(f"   Categories: {len(kb.get_all_categories())}")

    print(f"\n🎲 Random Samples:")
    product = kb.get_random_product()
    print(f"   Random Product: {product['name']}")

    category = kb.get_random_category()
    print(f"   Random Category: {category['name']}")

    print("\n✅ Knowledge base loaded successfully!\n")
    return kb

def test_tweet_generation(kb, num_tweets=5):
    """Generate test tweets."""
    print("=" * 60)
    print(f"GENERATING {num_tweets} TEST TWEETS")
    print("=" * 60)

    client = GrokClient(api_key=HF_TOKEN, model=HF_MODEL, temperature=0.7, max_tokens=150)
    prompt_builder = PromptBuilder(kb)

    generated_tweets = []

    for i in range(num_tweets):
        print(f"\n🤖 Tweet {i+1}/{num_tweets}")
        print("-" * 60)

        # Random parameters
        category = kb.get_random_category()
        length_type = random.choice(['short', 'long'])
        product = kb.get_random_product() if random.random() < 0.3 else None

        print(f"Category: {category['name']}")
        print(f"Length: {length_type}")
        if product:
            print(f"Product: {product['name']}")

        try:
            # Build prompts
            system_prompt = prompt_builder.build_system_prompt()
            user_prompt = prompt_builder.build_user_prompt(category, length_type, product)

            # Generate
            tweet = client.generate_tweet(system_prompt, user_prompt)

            # Clean
            import re
            tweet = tweet.strip('"\'')
            tweet = re.sub(r'^[-•]\s*', '', tweet, flags=re.MULTILINE)
            tweet = ' '.join(tweet.split())

            print(f"\n✅ Generated ({len(tweet)} chars):")
            print(f"   \"{tweet}\"")

            # Check for violations
            violations = []
            if any(emoji in tweet for emoji in ['🚀', '💜', '✅', '❌', '🎯', '📊']):
                violations.append("Contains emojis")
            if tweet.startswith('-') or tweet.startswith('•'):
                violations.append("Starts with bullet point")
            if len(tweet) > 280:
                violations.append(f"Too long ({len(tweet)} chars)")
            if len(tweet) < 50:
                violations.append(f"Too short ({len(tweet)} chars)")

            if violations:
                print(f"\n⚠️  Violations: {', '.join(violations)}")
            else:
                print(f"\n✅ No violations detected!")

            generated_tweets.append(tweet)

        except Exception as e:
            print(f"\n❌ Error: {e}")

    print("\n" + "=" * 60)
    print(f"✅ Generated {len(generated_tweets)}/{num_tweets} tweets successfully!")
    print("=" * 60)

    return generated_tweets

if __name__ == "__main__":
    # Test 1: Connection
    if not test_grok_connection():
        print("Fix Grok API connection before proceeding!")
        exit(1)

    # Test 2: Knowledge Base
    kb = test_knowledge_base()

    # Test 3: Tweet Generation
    tweets = test_tweet_generation(kb, num_tweets=5)

    print("\n🎉 All tests completed!")
    print("\nReady to run the bot with: python solana-hype-bot.py")
