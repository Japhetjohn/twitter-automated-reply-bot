class PromptBuilder:
    """
    Intelligent prompt construction for Grok API tweet generation.

    Builds system prompts with brand voice and user prompts with
    specific tweet requirements.
    """

    def __init__(self, knowledge_base):
        """
        Initialize prompt builder with knowledge base.

        Args:
            knowledge_base: NovaStaqKnowledgeBase instance
        """
        self.kb = knowledge_base

    def build_system_prompt(self):
        """
        Build comprehensive system prompt with brand voice.

        Returns:
            str: System prompt for Grok API
        """
        brand = self.kb.get_brand_voice_guidelines()
        rules = self.kb.get_strict_rules()

        system_prompt = f"""You are the official voice of Novastaq Technologies Inc on Twitter.

BRAND IDENTITY:
Novastaq is a blockchain technology company building decentralized payment infrastructure for Africa. We develop Web2 and Web3 solutions including payment systems, smart contracts, and financial infrastructure.

Products: Velcro (multi-currency fintech), BitNova (crypto P2P payments), Stakepadi (prediction markets), Tsara (settlement infrastructure), Criptpay (crypto payment gateway)

Mission: {brand.get('brand_identity', {}).get('mission', 'Build reliable digital infrastructure for payments and Web3 systems across Africa')}

VOICE & TONE:
Write in a professional, authoritative, and innovative voice. Be knowledgeable about blockchain, payments, and African tech. Sound confident but not arrogant. Be clear and accessible while maintaining technical credibility.

CRITICAL RULES - NEVER BREAK THESE:
1. NO emojis of any kind
2. NO bullet points, dashes, or list formatting
3. NO hashtags (unless specifically requested)
4. NO obvious AI patterns like "Excited to announce" or "Thrilled to share"
5. NO generic corporate speak or empty hype
6. Write naturally - sound human, not automated
7. Be specific and concrete - avoid vague generalities
8. Focus on insights rather than announcements
9. Provide genuine value to readers

CONTENT APPROACH:
Lead with substance, not promotion. If discussing products, explain the problem being solved. If sharing technical insights, make one clear point. If offering business wisdom, provide actionable lessons. If presenting thought leadership, make bold but defensible claims.

GOOD EXAMPLE:
"Cross-border payment fees in Africa average 8 to 10 percent. Blockchain can reduce this to under 1 percent. That is not innovation for innovation's sake, it is economic empowerment at scale."

BAD EXAMPLE:
"🚀 Excited to announce that blockchain is revolutionizing payments! Check out our amazing products! #Web3 #Africa"

Remember: Every tweet builds Novastaq's reputation. Be thoughtful, insightful, and genuinely valuable."""

        return system_prompt

    def build_user_prompt(self, category, length_type, product=None):
        """
        Build specific user prompt for tweet generation.

        Args:
            category: Category dict from knowledge base
            length_type: "short" (80-150 chars) or "long" (200-280 chars)
            product: Optional product dict to focus on

        Returns:
            str: User prompt for Grok API
        """
        category_name = category.get('name', '')
        category_desc = category.get('description', '')
        category_guidance = category.get('guidance', '')

        # Get length specifications with more variety
        length_specs = {
            'very_short': ("50-100 characters (ultra brief, punchy one-liner)",
                          "One sentence. Sharp and direct. Make every word count."),
            'short': ("100-150 characters (concise, quotable)",
                     "Brief but complete thought. Clear and impactful."),
            'medium': ("150-200 characters (balanced, informative)",
                      "Develop the idea with context. Two sentences work well."),
            'long': ("200-250 characters (detailed, explanatory)",
                    "Provide full context and reasoning. Multiple points if needed."),
            'very_long': ("250-280 characters (comprehensive, in-depth)",
                         "Maximum depth. Explain thoroughly with examples or data.")
        }

        length_spec, length_note = length_specs.get(length_type, length_specs['medium'])

        # Base prompt
        user_prompt = f"Generate a tweet for the '{category_name}' category.\n\n"

        # Add category context
        user_prompt += f"Category description: {category_desc}\n\n"

        # Add product focus if specified
        if product:
            product_name = product.get('name', '')
            product_desc = product.get('description', '')
            product_features = product.get('key_features', [])

            user_prompt += f"Focus on: {product_name}\n"
            user_prompt += f"Product: {product_desc}\n"

            if product_features and len(product_features) > 0:
                user_prompt += f"Consider features like: {', '.join(product_features[:3])}\n"

            user_prompt += "\n"

        # Add category-specific guidance
        if category_guidance:
            user_prompt += f"Approach: {category_guidance}\n\n"

        # Add example if available
        example = self.kb.get_random_category_example(category_name)
        if example:
            user_prompt += f"Example style (do not copy, just reference the approach):\n\"{example}\"\n\n"

        # Add length requirements
        user_prompt += f"Length: {length_spec}\n"
        user_prompt += f"{length_note}\n\n"

        # Final instructions
        user_prompt += "Generate ONE tweet that follows all the rules in the system prompt. "
        user_prompt += "Return ONLY the tweet text, nothing else. "
        user_prompt += "No quotation marks around the tweet. "
        user_prompt += "No emojis, no bullet points, no hashtags."

        return user_prompt

    def build_simple_fallback_prompt(self):
        """
        Build simpler prompt for fallback attempts.

        Returns:
            tuple: (system_prompt, user_prompt)
        """
        system_prompt = """You are tweeting for Novastaq, a blockchain technology company building payment infrastructure for Africa.

Rules:
- No emojis
- No bullet points
- No hashtags
- Sound professional and knowledgeable
- 100-250 characters
- Natural human voice"""

        user_prompt = """Write one tweet about blockchain technology, payments, or Web3 in Africa.

Make it insightful and valuable. Just return the tweet text, nothing else."""

        return system_prompt, user_prompt
