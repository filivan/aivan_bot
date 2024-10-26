import re
from aiogram import Router, F
from aiogram.enums import ParseMode, ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message
from loguru import logger
from utils import chat_completion


class MessageToBotFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        is_private = message.chat.type == ChatType.PRIVATE
        is_group = message.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}
        is_reply = (
            message.reply_to_message.from_user.id == message.bot.id
            if message.reply_to_message is not None
            else False
        )
        is_bot_mentioned = message.text.startswith(f"@{message.bot._me.username}")
        return is_private | is_group & (is_reply | is_bot_mentioned)


router = Router()


@router.message(F.text, MessageToBotFilter())
async def message_to_text_with_completion(message: Message):
    logger.info("Recived message from {user_id}", user_id=message.from_user.id)
    # await message.reply("Принял")
    try:
        completion = await chat_completion(
            message.text
            if not message.text.startswith(f"@{message.bot._me.username}")
            else message.text[len(f"@{message.bot._me.username}") :]
        )
        completion = re.sub(
            r"[_*[\]()~>#\+\-=|{}.!]", lambda x: "\\" + x.group(), completion
        )
        await message.reply(f"{completion}", parse_mode=ParseMode.MARKDOWN_V2)
        logger.info("Completion finished")

    except Exception as e:
        logger.exception(f"An error occurred")
