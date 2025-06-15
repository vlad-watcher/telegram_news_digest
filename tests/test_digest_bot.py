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
