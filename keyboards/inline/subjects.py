from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from loader import db

subject_cb = CallbackData("cb_register_subject", 'subject')


def get_subject_ikb(user_id):
    rows = db.select_user_subjects(user_id)

    keyboard = []
    buttons = []
    i = 0
    for row in rows:
        i += 1
        text = f'✅ {row[1]}' if row[2] else f'{row[1]}'
        buttons.append(
            InlineKeyboardButton(text=text, callback_data=subject_cb.new(subject=str(row[0])))
        )
        if i % 2 == 0:
            keyboard.append(buttons)
            buttons = []

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


test_subject_cb = CallbackData("cb_test_subject", 'id', 'name')


def get_test_subject_ikb():
    rows = db.select_subjects_2_tests()

    keyboard = []
    buttons = []
    i = 0
    for row in rows:
        i += 1
        text = f'{row[1]} ({row[2]})' if row[2] != 0 else f'{row[1]}'
        buttons.append(
            InlineKeyboardButton(text=text, callback_data=test_subject_cb.new(id=str(row[0]), name=row[1]))
        )
        if i % 2 == 0:
            keyboard.append(buttons)
            buttons = []

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
