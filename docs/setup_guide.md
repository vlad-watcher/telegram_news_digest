# Setup Guide

This guide walks you through configuring and running **Telegram News Digest** from scratch.

## 1. Prerequisites
- **Python 3.8 or later**
- A [Telegram API](https://my.telegram.org/) application ID and hash
- A Telegram bot created with [@BotFather](https://t.me/BotFather)
- Optionally, an OpenAI API key for better summarization

## 2. Clone the Repository
```bash
 git clone <repo-url>
 cd telegram_news_digest
```

## 3. Install Dependencies
It is recommended to use a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Configure Environment Variables
1. Copy the example file and open it for editing:
   ```bash
   cp .env.example .env
   nano .env  # or use your favourite editor
   ```
2. Fill in the following values:
   - `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` from your Telegram application
   - `BOT_TOKEN` for your bot
   - `TARGET_USER_ID` – your Telegram numeric ID (use `@userinfobot` to obtain it)
   - `CHANNELS` – comma-separated list of channel usernames or IDs to monitor
   - `CHANNEL_FETCH_LIMIT` (optional, default `10`) – number of posts retrieved from each channel
   - `OPENAI_API_KEY` (optional) for LLM-powered summaries
   - `OPENAI_MODEL` (optional, default `gpt-4o`)
   - `SUMMARY_TEMPERATURE` (optional, default `0.2`)
   - `SUMMARY_MAX_OUTPUT_TOKENS` (optional, default `1000`)
   - `SUMMARY_MAX_INPUT_TOKENS` (optional, default `5000`)

## 5. Run the Bot
Execute the main script to start the scheduler:
```bash
python main.py
```
The bot will fetch new posts every hour, create a digest and send it to the `TARGET_USER_ID`.

## 6. Updating Channels or Schedule
- Edit the `CHANNELS` value in `.env` to adjust the monitored channels.
- Modify the scheduling interval in `main.py` if you wish to run the digest more or less frequently.

## 7. Testing
Run the automated tests to verify your environment:
```bash
pytest -q
```
All tests should pass.

---
You are now ready to receive Telegram digests!

