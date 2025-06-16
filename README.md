# Telegram News Digest

Telegram News Digest is an AI agent that periodically gathers the most recent posts from a list of Telegram channels, summarizes them, and sends you a single private message containing the key information.

## Features
- Fetches the latest 20 posts from each configured channel
- Summarizes posts into one concise digest
- Sends the digest to a target Telegram user via bot DM
- Easily configurable list of channels and schedule

## Getting Started
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   ```
2. **Install dependencies** (Python 3.8+ recommended)
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment**
   - Copy `.env.example` to `.env` and fill in your credentials:
     - `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` – credentials for a Telegram application
     - `BOT_TOKEN` – your bot token
     - `TARGET_USER_ID` – user ID to receive digests
     - `CHANNELS` – comma-separated list of channel usernames
    - Optional summarization settings:
      - `OPENAI_API_KEY` – required for OpenAI-based summaries
      - `OPENAI_MODEL` – model name (default `gpt-4o`)
      - `SUMMARY_TEMPERATURE` – sampling temperature (default `0.2`)
      - `SUMMARY_MAX_OUTPUT_TOKENS` – maximum summary tokens (default `1000`)
      - `SUMMARY_MAX_INPUT_TOKENS` – maximum input tokens considered (default `5000`)
4. **Run the bot**
   ```bash
   python main.py
   ```

### Running with Docker

Alternatively you can run the bot inside a container. Build the image and pass
your `.env` file when starting the container:

```bash
docker build -t telegram-digest .
docker run --env-file .env telegram-digest
```

For a more in-depth walkthrough including environment setup, see
[the setup guide](docs/setup_guide.md).

## Project Structure
- `docs/design.md` – detailed design document describing architecture and implementation steps
- `main.py` – entry point that runs the scheduled digest bot
- `requirements.txt` – Python dependencies

## Contributing
Contributions are welcome! Please open issues or submit pull requests to suggest features or fixes.

## License
This project is licensed under the [MIT License](LICENSE).

