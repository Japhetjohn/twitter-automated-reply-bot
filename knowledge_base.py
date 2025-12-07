import json
import os
import random


class NovaStaqKnowledgeBase:
    """
    Centralized knowledge management system for Novastaq content.

    Loads and provides access to products, brand voice, content categories,
    and whitepaper data.
    """

    def __init__(self, knowledge_dir="knowledge"):
        """
        Initialize knowledge base and load all data.

        Args:
            knowledge_dir: Directory containing JSON knowledge files
        """
        self.knowledge_dir = knowledge_dir
        self.products = []
        self.brand_voice = {}
        self.categories = []
        self.whitepaper = {}

        self.load_all_data()

    def load_all_data(self):
        """Load all JSON knowledge files."""
        try:
            # Load products
            with open(os.path.join(self.knowledge_dir, "products.json"), 'r') as f:
                data = json.load(f)
                self.products = data.get('products', [])
                print(f"[OK] Loaded {len(self.products)} products")

            # Load brand voice
            with open(os.path.join(self.knowledge_dir, "brand_voice.json"), 'r') as f:
                self.brand_voice = json.load(f)
                print(f"[OK] Loaded brand voice guidelines")

            # Load content categories
            with open(os.path.join(self.knowledge_dir, "content_categories.json"), 'r') as f:
                data = json.load(f)
                self.categories = data.get('categories', [])
                print(f"[OK] Loaded {len(self.categories)} content categories")

            # Load whitepaper data
            with open(os.path.join(self.knowledge_dir, "whitepaper_data.json"), 'r') as f:
                self.whitepaper = json.load(f)
                print(f"[OK] Loaded whitepaper data")

        except FileNotFoundError as e:
            print(f"[ERROR] Knowledge file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in knowledge file: {e}")
            raise

    def get_random_product(self):
        """
        Get a random product from the knowledge base.

        Returns:
            dict: Random product with all details
        """
        if not self.products:
            return None
        return random.choice(self.products)

    def get_product_by_name(self, name):
        """
        Get specific product by name.

        Args:
            name: Product name (e.g., "Velcro", "BitNova")

        Returns:
            dict: Product details or None if not found
        """
        for product in self.products:
            if product['name'].lower() == name.lower():
                return product
        return None

    def get_random_category(self):
        """
        Get a random category based on weights.

        Categories with higher weights are selected more frequently.

        Returns:
            dict: Random category with details
        """
        if not self.categories:
            return None

        # Extract weights
        weights = [cat.get('weight', 1.0) for cat in self.categories]

        # Weighted random selection
        return random.choices(self.categories, weights=weights, k=1)[0]

    def get_category_by_name(self, name):
        """
        Get specific category by name.

        Args:
            name: Category name (e.g., "product_spotlight")

        Returns:
            dict: Category details or None if not found
        """
        for category in self.categories:
            if category['name'].lower() == name.lower():
                return category
        return None

    def get_brand_voice_guidelines(self):
        """
        Get brand voice and tone guidelines.

        Returns:
            dict: Brand voice data including tone, rules, examples
        """
        return self.brand_voice

    def get_random_category_example(self, category_name):
        """
        Get a random example tweet from a specific category.

        Args:
            category_name: Name of the category

        Returns:
            str: Random example tweet or None
        """
        category = self.get_category_by_name(category_name)
        if category and 'examples' in category and category['examples']:
            return random.choice(category['examples'])
        return None

    def get_whitepaper_snippet(self, section=None):
        """
        Get a specific section from whitepaper or random insight.

        Args:
            section: Specific section name or None for random

        Returns:
            str or dict: Whitepaper content
        """
        if section and section in self.whitepaper:
            return self.whitepaper[section]

        # Return random key insight
        if 'key_insights' in self.whitepaper and self.whitepaper['key_insights']:
            return random.choice(self.whitepaper['key_insights'])

        return None

    def get_all_products(self):
        """Get list of all products."""
        return self.products

    def get_all_categories(self):
        """Get list of all categories."""
        return self.categories

    def get_strict_rules(self):
        """
        Get strict content rules (what to avoid, what to follow).

        Returns:
            dict: Strict rules from brand voice
        """
        return self.brand_voice.get('strict_rules', {})

    def get_example_good_tweets(self):
        """Get examples of good tweets for reference."""
        return self.brand_voice.get('example_good_tweets', [])

    def get_example_bad_tweets(self):
        """Get examples of bad tweets to avoid."""
        return self.brand_voice.get('example_bad_tweets', [])

    def get_web3_education_topic(self):
        """Get a random Web3 education topic."""
        topics = self.whitepaper.get('web3_education_topics', [])
        return random.choice(topics) if topics else None

    def get_market_insight(self):
        """Get a random market opportunity insight."""
        market_data = self.whitepaper.get('market_opportunity', {})
        if market_data:
            key = random.choice(list(market_data.keys()))
            return {key: market_data[key]}
        return None
