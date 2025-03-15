import asyncio
from aiogram import Bot, Dispatcher
from loguru import logger
from handlers import base, speech, chat, vision
from config import settings
from middlewares import AuthMiddleware


async def main() -> None:
    """
    Main entry point for the bot. Create a Bot and Dispatcher, include
    all routers and start polling.
    """
    print(settings.BOT_TOKEN)
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.update.middleware(AuthMiddleware())

    # Include all the routers
    dp.include_routers(base.router, chat.router, speech.router, vision.router)

    # Remove existing webhook (skip current messages) and start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Bot started")
    asyncio.run(main())
