from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

settings_cb = CallbackData('settings_menu', 'menu')


settings_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="To'liq ism", callback_data=settings_cb.new(menu='name')),
            InlineKeyboardButton(text="Telefon", callback_data=settings_cb.new(menu='phone'))
        ],
        [
            InlineKeyboardButton(text="Viloyat", callback_data=settings_cb.new(menu='region')),
            InlineKeyboardButton(text="Universitet", callback_data=settings_cb.new(menu='university'))
        ]
    ],
)
