import asyncio
from aiogram import Bot, Dispatcher
from loguru import logger
from handlers import base, speech, chat
from config import settings


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        base.router,
        chat.router,
        speech.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Bot started")
    asyncio.run(main())
