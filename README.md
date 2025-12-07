# Novastaq AI Twitter Bot

Intelligent Twitter bot for Novastaq Technologies powered by Hugging Face AI. Automatically generates and posts professional tweets about Novastaq products, Web3 technology, and African tech ecosystem.

## Features

- AI-powered tweet generation using Hugging Face LLM (free tier)
- 4 content categories: Product spotlight, Tech insights, Business wisdom, Thought leadership
- Smart scheduling: 3-5 tweets per day with 2-6 hour gaps
- No night posting (sleeps from 11 PM to 8 AM)
- Automatic duplicate prevention with tweet history
- Natural, professional language (no emojis, no bullet points)
- 5 length variations: very short to very long (50-280 characters)

## Setup

### Prerequisites

- Python 3.8+
- Twitter Developer Account with API credentials
- Hugging Face account with API token

### Installation

1. Clone or download the repository

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure credentials - Create `.env` file:

```bash
# Twitter API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# Hugging Face API
HF_TOKEN=your_hf_token_here
HF_MODEL=meta-llama/Llama-3.3-70B-Instruct
HF_TEMPERATURE=0.7
HF_MAX_TOKENS=150
```

## Usage

### Run the Bot
```bash
python solana-hype-bot.py
```

### Run in Background
```bash
nohup python solana-hype-bot.py > bot.log 2>&1 &
```

### Stop Background Bot
```bash
pkill -f solana-hype-bot.py
```

## Project Structure

```
twitter-bot/
├── solana-hype-bot.py       # Main bot
├── grok_client.py            # LLM API client
├── knowledge_base.py         # Content manager
├── prompt_builder.py         # Prompt engineer
├── knowledge/                # Data directory
│   ├── products.json
│   ├── brand_voice.json
│   ├── content_categories.json
│   └── whitepaper_data.json
├── test_run.py              # Test posting
├── requirements.txt         # Dependencies
├── .env                     # Credentials
└── README.md               # Documentation
```

## Configuration

Edit posting frequency in `solana-hype-bot.py`:
```python
TWEETS_PER_DAY = random.randint(3, 5)
```

Change AI model in `.env`:
```bash
HF_MODEL=meta-llama/Llama-3.3-70B-Instruct
```

Adjust creativity in `.env`:
```bash
HF_TEMPERATURE=0.7  # 0.0-1.0
```

## Content Categories

1. Product Spotlight (25%) - Novastaq products
2. Tech/Engineering (25%) - Technical insights
3. Startup/Business (20%) - Business wisdom
4. Thought Leadership (30%) - Industry trends

## Tweet Lengths

- Very Short (50-100 chars)
- Short (100-150 chars)
- Medium (150-200 chars)
- Long (200-250 chars)
- Very Long (250-280 chars)

## Troubleshooting

**Missing credentials**: Verify all keys in `.env`

**API errors**: Check internet and HF token validity

**Repetitive tweets**: Lower temperature in `.env`

## License

Proprietary - Novastaq Technologies Inc.
