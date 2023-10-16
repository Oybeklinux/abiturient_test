from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db
from utils.misc.mix import row_2_col


def get_exam_main_kb(user_id):
    rows = db.select_chosen_subjects(user_id)
    rows = row_2_col(rows)
    buttons = []
    keyboard = []
    for columns in rows:
        for column in columns:
            buttons.append(
                KeyboardButton(text=column[1])
            )
        keyboard.append(buttons)
        buttons = []
    keyboard[-1].append(KeyboardButton(text="⬅️ Orqaga"))
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)

