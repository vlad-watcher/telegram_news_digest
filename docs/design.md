# Telegram News Digest Design Document

## Objective
Create an AI-driven Telegram agent that periodically retrieves the latest 20 posts from each Telegram channel in a predefined list, summarizes the gathered posts, and delivers a concise digest to a specified user via a private message.

## High-Level Overview
1. **Data Collection**
   - Use the Telegram API to fetch the most recent 20 posts from each channel.
   - Schedule periodic polling (e.g., hourly) using a task scheduler.

2. **Summarization**
   - Aggregate posts and generate a summary using an LLM (Large Language Model) or heuristic summarization.
   - Ensure messages from multiple channels are merged into one digest.

3. **Delivery**
   - Send the digest as a single message to the target user via the Telegram Bot API.

## Architecture
- **Bot Component**: Handles authentication, channel fetching, and message delivery.
- **Scheduler**: Triggers periodic execution. Could use cron, `apscheduler`, or similar.
- **Summarization Module**: Encapsulates summarization logic, optionally leveraging external APIs for LLM-based summarization.

### Data Flow
1. Scheduler triggers bot.
2. Bot fetches posts from each channel.
3. Posts are passed to Summarization Module.
4. Summaries are composed into one digest.
5. Bot delivers digest to user.

## Implementation Steps
1. **Set Up Bot**
   - Register a Telegram bot and obtain the bot token.
   - Store configuration (token, target channels, user ID) in environment variables or config file.

2. **Fetch Posts**
   - Use Telegram Client libraries such as `telethon` or `pyrogram`.
   - Implement logic to track the latest processed post ID for each channel to avoid duplicates.

3. **Summarize**
   - Combine fetched posts and summarize them using an LLM API (e.g., OpenAI) or an open-source model.
   - Include error handling for API failures.

4. **Deliver Digest**
   - Send a single message with the summarized content via the Telegram Bot API.

5. **Scheduling**
   - Use `cron` or `apscheduler` to run the fetch-summarize-send cycle periodically.

6. **Logging & Monitoring**
   - Log activity for debugging and auditing.
   - Optionally provide metrics on fetch and summarization operations.

7. **Testing & Deployment**
   - Unit tests for summarization and message formatting.
   - Integration tests for fetching and sending messages with a mock Telegram API.
   - Containerize the application for deployment.

## Future Enhancements
- Add database persistence for posts and summaries.
- Support different summarization modes (bullet points, headlines).
- Extend to multiple users or dynamic channel lists.

