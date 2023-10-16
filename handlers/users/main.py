from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.default.exam import get_exam_main_kb
from keyboards.default.main import extra_kb
from loader import dp


@dp.message_handler(Text(equals='🧑‍💻 Test imtihoni'))
async def exam_start(message: types.Message):
    user_id = message.from_user.id
    await message.answer(text='Fanlardan birini tanlang', reply_markup=get_exam_main_kb(user_id))


@dp.message_handler(Text(equals='⬅️ Orqaga'))
async def exam_start(message: types.Message):
    user_id = message.from_user.id
    await message.answer(text='', reply_markup=get_exam_main_kb(user_id))


@dp.message_handler(Text(equals='✔ Imtihon javoblari'))
async def exam_result(message: types.Message):
    pass


@dp.message_handler(Text(equals="➡️ Ko'proq"))
async def more_kb(message: types.Message):
    await message.answer(text="Bu bo'limda siz profilni o'zgartirish, fanlarni tanlash va texnik yordamni foydalanishingiz mumkin",
                         reply_markup=extra_kb)