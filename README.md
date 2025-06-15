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
   - Create a `.env` file with your Telegram bot token, target channels, and user ID.
   - Optional: add API keys for your preferred LLM provider if using external summarization services.
4. **Run the bot**
   ```bash
   python main.py
   ```

## Project Structure
- `docs/design.md` – detailed design document describing architecture and implementation steps
- `main.py` – entry point (to be implemented)
- `requirements.txt` – Python dependencies

## Contributing
Contributions are welcome! Please open issues or submit pull requests to suggest features or fixes.

## License
This project is licensed under the MIT License.

