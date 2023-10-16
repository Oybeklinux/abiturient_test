from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                  keyboard=[[
    KeyboardButton(text="📱 Kontaktni yuborish", request_contact=True)
]])