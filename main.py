import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from dotenv import load_dotenv
from faststream.rabbit import RabbitBroker

load_dotenv()
# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")
RABBIT_URL = getenv("RABBIT_BROKER_URL", "amqp://guest:guest@rabbitmq:5672/")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

rabbit_broker = RabbitBroker(RABBIT_URL)


@rabbit_broker.subscriber("orders")
async def handle_products(data: str):
    await bot.send_message(
        chat_id=5772642683,
        text=data
    )

async def wait_for_rabbit(max_retries=10, delay=3):
    for attempt in range(max_retries):
        try:
            logging.info(f"Trying to connect to RabbitMQ... (attempt {attempt + 1})")
            await rabbit_broker.connect()
            logging.info("RabbitMQ is available!")
            return
        except Exception as e:
            logging.warning(f"RabbitMQ not ready: {e}")
            await asyncio.sleep(delay)
    raise Exception("RabbitMQ never became available.")

async def main() -> None:
    await wait_for_rabbit()
    async with rabbit_broker:
        await rabbit_broker.start()
        logging.info("Broker is up and running")
        await dp.start_polling(bot)
    logging.info("Broker is done. Exit.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
