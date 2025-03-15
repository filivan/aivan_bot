from aiogram import F, Router
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, MEMBER
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram.enums import ChatType
from loguru import logger
from keyboards import inline_get_access_keyboard
from config import settings


router = Router()


class AuthStates(StatesGroup):
    waiting_for_password = State()


START_MESSAGE = "✋ Привет, я {bot_full_name}! Я твой универсальный и удобный в использовании ИИ-ассистент 🤖.\n\
⏳ На данный момент, я могу выполнять все функции, которые доступны современным языковым моделям (LLM):\n\
    - Отвечать на вопросы, помогать в генерации контента, идей, кода etc.;\n\
    - Переводить аудиосообщения в текст;\n\
    - Отвечать на вопросы по изображениям.\n\n\
Ты можешь общаться со мной здесь или добавить меня в группу.\n\n\
Просто напиши мне, отправь изображение указав в подписи, что нужно сделать или перешли мне аудиосообщение.\n\n\
Если добавить меня в группу, я буду отслеживать аудиосообщения и автоматически переводить их в текст.\n\n\
Чтобы я ответил в группе, начни сообщение с обращения ко мне @{bot_username} или задай вопрос в ответе на моё сообщение!\n\n"
ACCES_MESSAGE = 'Но для начала нажми кнопку "ПОЛУЧИТЬ ДОСТУП" и введи пароль.\''


@router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info(f"User {message.from_user.id} started bot")
    start_answer = START_MESSAGE.format(
        bot_full_name=message.bot._me.full_name,
        bot_username=message.bot._me.username,
    )
    reply_markup = None
    if message.from_user.id not in settings.AUTHORIZED_USERS_ID:
        start_answer += ACCES_MESSAGE
        reply_markup = inline_get_access_keyboard
    await message.answer(
        start_answer,
        reply_markup=reply_markup,
    )


@router.callback_query(F.data == "get_access")
async def request_password(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Введите пароль:")
    await state.set_state(AuthStates.waiting_for_password)


@router.message(AuthStates.waiting_for_password)
async def check_password(message: Message, state: FSMContext):
    if message.text == settings.ACCESS_PASSWORD:
        settings.AUTHORIZED_USERS_ID.add(message.from_user.id)
        await message.reply(
            "Доступ открыт! Теперь вы можете в полной мере пользоваться ботом и добавлять его в группы."
        )
        await state.clear()  # Reset FSM state after successful authentication
    else:
        await message.reply(
            'Неправильный пароль. Нажмите кнопку "ПОЛУЧИТЬ ДОСТУП" и введите пароль ещё раз.',
            reply_markup=inline_get_access_keyboard,
        )
        await state.clear()  # Reset state in case of incorrect password


@router.my_chat_member(
    F.chat.type != ChatType.PRIVATE,
    ChatMemberUpdatedFilter(member_status_changed=MEMBER),
)
async def added_to_group(event: ChatMemberUpdated) -> None:
    logger.info(f"Bot was added to group {event.chat.id} by user {event.from_user.id}")
    settings.AUTHORIZED_CHATS_ID.add(event.chat.id)
