from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

main_kb = ReplyKeyboardMarkup(resize_keyboard=True,
  keyboard=[
    [
      KeyboardButton(text="🧑‍💻 Test imtihoni"),
      KeyboardButton(text="✔ Imtihon javoblari")
    ],
    [
      KeyboardButton(text='🌐 "Kelajagim" ilovasi',web_app=types.WebAppInfo(url="https://play.google.com/store/apps/details?id=com.bodhistudentdemo.in&hl=en&gl=US") ),
      KeyboardButton(text="➡️ Ko'proq")
    ],
  ])

extra_kb = ReplyKeyboardMarkup(resize_keyboard=True,
  keyboard=[
    [
      KeyboardButton(text="✏️Profilni o'zgartirish"),
      KeyboardButton(text="🛠 Texnik yordam")
    ],
    [
      KeyboardButton(text='✔ Fanlarni tanlash'),
      KeyboardButton(text="⬅️ Orqaga")
    ],
  ])
