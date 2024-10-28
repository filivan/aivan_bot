import telegramify_markdown
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from loguru import logger
from filters import MessageToBotFilter
from utils import chat_completion


router = Router()


@router.message(F.text, MessageToBotFilter())
async def message_to_text_with_completion(message: Message):
    logger.info("Recived message from {user_id}", user_id=message.from_user.id)
    try:
        completion = await chat_completion(
            message.text
            if not message.text.startswith(f"@{message.bot._me.username}")
            else message.text[len(f"@{message.bot._me.username}") :]
        )
        completion = telegramify_markdown.markdownify(completion)
        await message.reply(f"{completion}", parse_mode=ParseMode.MARKDOWN_V2)
        logger.info("Completion finished")

    except Exception:
        logger.exception("An error occurred")
        await message.reply("An error occurred")
