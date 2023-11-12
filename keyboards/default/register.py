from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                  keyboard=[[
    KeyboardButton(text="✅ Ro'yxatdan o'tish")
]])

register2_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                  keyboard=[[
    KeyboardButton(text="✏️Profilni o'zgartirish"),
    KeyboardButton(text="✔ Fanlarni tanlash")
]])

select_subject_confirm_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                  keyboard=[[
    KeyboardButton(text="✅ Tasdiqlash")
]])


