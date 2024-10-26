from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info(f"User {message.from_user.id} started bot")
    await message.answer("Привет, герой!")
