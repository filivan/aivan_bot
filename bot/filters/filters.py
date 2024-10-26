from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message


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
