import asyncio
import logging
import os
from datetime import datetime
from typing import List

from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from digest_bot import DigestBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


def get_env_list(name: str) -> List[str]:
    value = os.getenv(name, "")
    return [v.strip() for v in value.split(",") if v.strip()]


def run_job(bot: DigestBot):
    logger.info("Running digest cycle at %s", datetime.utcnow())
    asyncio.run(bot.run_cycle())


def main():
    api_id = int(os.getenv("TELEGRAM_API_ID"))
    api_hash = os.getenv("TELEGRAM_API_HASH")
    bot_token = os.getenv("BOT_TOKEN")
    target_user = int(os.getenv("TARGET_USER_ID"))
    channels = get_env_list("CHANNELS")

    bot = DigestBot(api_id, api_hash, bot_token, target_user, channels)

    scheduler = BlockingScheduler()
    scheduler.add_job(run_job, "interval", hours=1, args=[bot])
    logger.info("Starting scheduler...")
    scheduler.start()


if __name__ == "__main__":
    main()
