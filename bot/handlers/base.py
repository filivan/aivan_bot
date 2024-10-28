from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

router = Router()

START_MESSAGE = "✋ Привет, я AIvan! Я твой универсальный и удобный в использовании ИИ-ассистент 🤖.\n\
⏳ На данный момент, я могу выполнять все функции, которые доступны современным языковым моделям (LLM), а также переводить аудиосообщения в текст.\n\n\
Ты можешь общаться со мной здесь или добавить меня в группу.\n\n\
Просто перешли мне аудиосообщение или напиши мне.\n\n\
Если добавить меня в группу, я буду отслеживать аудиосообщения и автоматически переводить их в текст.\n\n\
Чтобы я ответил в группе, начни сообщение с обращения ко мне @{bot_name} или задай вопрос в ответе на моё сообщение!\n"


@router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info(f"User {message.from_user.id} started bot")
    await message.answer(START_MESSAGE.format(bot_name=message.bot._me.username))
