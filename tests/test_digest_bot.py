import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from digest_bot import DigestBot


class DummyBot(DigestBot):
    def __init__(self):
        super().__init__(api_id=1, api_hash="hash", bot_token="token", target_user=1, channels=[])

    async def fetch_posts(self):
        return {"channel1": ["msg1", "msg2"], "channel2": ["msg3"]}


def test_summarize_format():
    bot = DummyBot()
    digest = bot.summarize({"ch": ["a", "b"]})
    assert isinstance(digest, str)
    assert "ch" in digest


class DummyMessage:
    def __init__(self, id: int, message: str):
        self.id = id
        self.message = message


class DummyClient:
    def __init__(self, messages):
        self.messages = messages

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def iter_messages(self, channel, limit=20):
        async def gen():
            for msg in self.messages.get(channel, []):
                yield msg

        return gen()


class StatefulBot(DigestBot):
    def __init__(self, messages):
        super().__init__(api_id=1, api_hash="hash", bot_token="token", target_user=1, channels=list(messages.keys()))
        self.client = DummyClient(messages)
        self.sent = []

    def _load_state(self):
        return {}

    def _save_state(self):
        pass

    def send_digest(self, digest: str):
        self.sent.append(digest)


import pytest
import asyncio
import digest_bot as digest_bot_module


def test_run_cycle_deduplicates(monkeypatch):
    monkeypatch.setattr(digest_bot_module, "Message", DummyMessage)
    msgs = {"chan": [DummyMessage(3, "m3"), DummyMessage(2, "m2"), DummyMessage(1, "m1")]} 
    bot = StatefulBot(msgs)

    asyncio.run(bot.run_cycle())
    assert bot.state["chan"] == 3
    assert len(bot.sent) == 1

    # No new messages should be fetched on the next cycle
    asyncio.run(bot.run_cycle())
    assert len(bot.sent) == 1
