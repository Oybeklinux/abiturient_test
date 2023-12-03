from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


def get_tests_kb(all_tests, answered_tests=[], current_test_id=None):
    keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                          selective=True,
                                          row_width=6,
                                          input_field_placeholder='Savol raqamini tanlang yoki yozing',
                                          is_persistent=True)
    i = 1
    for test_id in all_tests:
        if test_id == current_test_id:
            text = f"📍{i}"
        elif test_id in answered_tests:
            text = f"✅{i}"

        else:
            text = f"{i}"
        i += 1

        keyboard_markup.insert(
            KeyboardButton(text=text)
        )
    keyboard_markup.insert(
        KeyboardButton(text="⬅ Orqaga")
    )
    return keyboard_markup
