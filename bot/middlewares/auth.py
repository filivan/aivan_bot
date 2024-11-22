from collections.abc import Awaitable, Callable
from typing import Any
from aiogram import BaseMiddleware
from aiogram.types import (
    Message,
    Update,
    CallbackQuery,
    User,
    ChatMemberUpdated,
    Chat,
    ContentType,
)
from aiogram.enums import ChatMemberStatus, ChatType
from config import settings

from aiogram.fsm.state import State, StatesGroup


class AuthStates(StatesGroup):
    waiting_for_password = State()


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        event_from_user: User | None = data.get("event_from_user")
        event_chat: Chat | None = data.get("event_chat")
        if (
            event_from_user is not None
            and event_from_user.id in settings.AUTHORIZED_USERS_ID
            or event_chat.id in settings.AUTHORIZED_CHATS_ID
        ):
            return await handler(event, data)

        if isinstance(event.event, Message) and event.message.text == "/start":
            return await handler(event, data)

        if (
            isinstance(event.event, CallbackQuery)
            and event.callback_query.data == "get_access"
        ):
            return await handler(event, data)

        fsm_context = data.get("state")
        state = await fsm_context.get_state()
        if state == AuthStates.waiting_for_password.state:
            return await handler(event, data)

        if (
            isinstance(event.event, ChatMemberUpdated)
            and event.event_type == "my_chat_member"
            and event.event.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}
            and event.event.new_chat_member.status == ChatMemberStatus.MEMBER
            and event_from_user not in settings.AUTHORIZED_USERS_ID
        ):
            await event.event.answer("Доступ запрещен!")
            await event.bot.leave_chat(event.event.chat.id)
        if event.message is not None and event.message.content_type not in {
            ContentType.NEW_CHAT_MEMBERS,
            ContentType.LEFT_CHAT_MEMBER,
        }:
            await event.message.answer("Доступ запрещен!")
        return
        # logger.info(f"new user registration | user_id: {user.id} | message: {message.text}")
