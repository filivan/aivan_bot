import asyncio
from aiogram import Bot, Dispatcher
from loguru import logger
from handlers import base, transcript
from settings import settings

logger.add("log/log.debug", level="DEBUG")
logger.add("log/log.warn", level="WARNING")

# Запуск бота
async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(transcript.router,
                       base.router)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Bot started")
    asyncio.run(main())