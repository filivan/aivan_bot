from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_get_access_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Get Access", callback_data="get_access")]
    ]
)
