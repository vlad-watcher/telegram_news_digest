"""Telegram digest bot utilities."""

import json
import logging
import os
from pathlib import Path
from typing import List, Dict

import requests
from telethon import TelegramClient
from telethon.tl.custom import Message

from summarizer import summarize_texts

logger = logging.getLogger(__name__)


class DigestBot:
    """Fetches posts from Telegram channels and sends a summarized digest."""

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        bot_token: str,
        target_user: int,
        channels: List[str],
        state_path: str = "state.json",
    ) -> None:
        """Create a new :class:`DigestBot`.

        Args:
            api_id: Telegram API ID.
            api_hash: Telegram API hash.
            bot_token: Bot token used for sending messages.
            target_user: ID of the user who receives digests.
            channels: Channel usernames or IDs to monitor.
            state_path: Path to the JSON file storing last processed IDs.
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.target_user = target_user
        self.channels = channels
        self.client = TelegramClient("digest", api_id, api_hash)
        self.state_path = Path(state_path)
        self.state: Dict[str, int] = self._load_state()

    def _load_state(self) -> Dict[str, int]:
        if self.state_path.exists():
            try:
                with self.state_path.open("r") as fh:
                    return json.load(fh)
            except Exception as exc:
                logger.error("Failed to load state file: %s", exc)
        return {}

    def _save_state(self):
        try:
            with self.state_path.open("w") as fh:
                json.dump(self.state, fh)
        except Exception as exc:
            logger.error("Failed to save state file: %s", exc)

    async def fetch_posts(self) -> Dict[str, List[str]]:
        """Fetch new posts from configured channels.

        Returns:
            A mapping of channel names to lists of message strings.
        """

        messages = {}
        async with self.client:
            for channel in self.channels:
                last_id = self.state.get(channel, 0)
                fetched = []
                highest_id = last_id
                async for msg in self.client.iter_messages(channel, limit=20):
                    if isinstance(msg, Message) and msg.id > last_id:
                        if msg.message:
                            fetched.append(msg.message)
                        if msg.id > highest_id:
                            highest_id = msg.id
                    if len(fetched) >= 20:
                        break
                if fetched:
                    self.state[channel] = highest_id
                    messages[channel] = list(reversed(fetched))
        self._save_state()
        return messages

    def summarize(self, messages: Dict[str, List[str]]) -> str:
        """Create a summary digest from fetched messages."""

        texts = []
        for channel, msgs in messages.items():
            texts.append(f"Channel: {channel}")
            texts.extend(msgs)
            texts.append("")
        return summarize_texts(texts)

    def send_digest(self, digest: str) -> None:
        """Send the digest message to the target user."""

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.target_user, "text": digest}
        resp = requests.post(url, data=payload, timeout=10)
        if resp.status_code != 200:
            logger.error("Failed to send digest: %s", resp.text)

    async def run_cycle(self):
        """Run one fetch/summarize/send cycle."""

        posts = await self.fetch_posts()
        if not posts:
            logger.info("No new posts fetched")
            return
        digest = self.summarize(posts)
        self.send_digest(digest)
