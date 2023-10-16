from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from loader import db
from utils.misc.mix import row_2_col

region_cb = CallbackData("cb_register_region", 'region')


def get_region_ikb():
    rows = db.select_regions()
    rows = row_2_col(rows)
    keyboard = []
    buttons = []
    for columns in rows:
        for column in columns:
            buttons.append(
                InlineKeyboardButton(text=f'{column[1]}', callback_data=region_cb.new(region=str(column[0])))
            )

        keyboard.append(buttons)
        buttons = []

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )



# confirm_cb = CallbackData("cb_register_confirm", "submenu")
# confirm_ikb = InlineKeyboardMarkup(
#                                   inline_keyboard=[[
#     InlineKeyboardButton(text="✅ Tasdiqlash",callback_data=confirm_cb.new(submenu='confirm')),
#     InlineKeyboardButton(text="❌ Bekor qilish", callback_data=confirm_cb.new(submenu='cancel'))
# ]])