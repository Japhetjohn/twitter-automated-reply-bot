# 🔗 Twitter Bot for Blockchain Developers (FREE TIER)

Automated Twitter bot for blockchain devs - optimized for FREE TIER (50 tweets/month limit)

## 🎯 What It Does

- **70% Replies** - Responds to blockchain/crypto/web3 tweets
- **30% Retweets** - Shares relevant content
- **NO Original Tweets** - Conserves API usage

**FREE TIER OPTIMIZED:**
- 2 actions per day max
- 45 actions per month limit (safely under 50)
- 5-15 minute delays between actions
- Uses Twitter API v2 (free tier compatible)
- Tracks daily and monthly usage

## 🚀 Quick Start

1. **Install dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Setup credentials:**
Create a `.env` file with your Twitter API credentials:
```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

3. **Run the bot:**
```bash
./start-bot.sh
```

## 🔑 Getting Twitter API Credentials

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new App
3. Get these credentials:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret
   - Bearer Token

**Note:** Free tier only allows 50 tweets/month. This bot is optimized for that limit.

## ✅ Pre-Configured Features

### 50+ Blockchain/Web3 Keywords
- Major chains: ethereum, solana, bitcoin, cardano, polygon, avalanche
- L2s: arbitrum, optimism, zksync, starknet
- DeFi: uniswap, aave, compound
- Dev tools: solidity, rust, blockchain development
- Topics: smart contracts, gas optimization, web3 dev

### 40+ Engaging Reply Templates
- "This is actually a solid approach 🔥"
- "WAGMI 💪"
- "Facts bro 💯"
- "Love the gas efficiency approach 💰"
- And 35+ more natural, engaging replies

## 📁 Files

```
twitter-bot/
├── twitter-bot.py        ← Main bot (API v2)
├── start-bot.sh         ← Start script
├── test-credentials.py  ← Test your API
├── requirements.txt     ← Dependencies
└── README.md            ← This file
```

## 📊 How It Works

```
Search tweets → Filter → Random selection → Reply/Retweet
     ↓            ↓            ↓                ↓
  API v2    Your own    30% of tweets    70% reply
  search     tweets      selected        30% retweet
             excluded
```

## ⚠️ Important

### FREE Tier Limits
- **50 tweets/month** write limit
- Bot does **2 actions/day** = ~60/month
- Auto-stops at **45/month** to stay safe

### Rate Limits
- Search: 10 requests per 15 minutes
- Bot auto-handles limits and sleeps when needed

### Security
- **NEVER commit .env file** - it has your API keys!
- The `.gitignore` protects your secrets
- Keep your credentials private

## 🔥 Features

- ✅ Twitter API v2 compatible (free tier)
- ✅ Random 5-15 minute delays
- ✅ Daily and monthly tracking
- ✅ Auto-stops at limits
- ✅ Filters own tweets
- ✅ No duplicates
- ✅ Natural, human-like behavior

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "403 Forbidden" | You need API v2 access (free tier has this) |
| "Rate limit exceeded" | Normal! Bot will sleep and retry |
| "Daily limit reached" | Working as intended, resumes tomorrow |
| Import errors | Run `pip install -r requirements.txt` |

## ⚖️ Legal Notice

For legitimate use only:
- ✅ Personal brand building
- ✅ Developer engagement
- ✅ Community participation
- ❌ Spam or manipulation

Use responsibly and comply with Twitter's Terms of Service.

---

**Ready to go!** Just configure `.env` and run `./start-bot.sh` 🚀
