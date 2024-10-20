from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

router = Router()

@router.message(F.voice)
async def message_to_audio_with_transcription(message: Message):
    logger.info(f"Recived voice message from {message.from_user.id}")
    await message.reply("Принял")