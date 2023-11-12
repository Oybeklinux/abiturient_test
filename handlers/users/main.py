from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default.exam import get_subjects_kb
from keyboards.default.main import extra_kb, main_kb
from loader import dp
from states.menu_state import MenuState


@dp.message_handler(Text(equals='🧑‍💻 Test imtihoni'))
async def exam_start(message: types.Message, state:FSMContext):
    await state.update_data(menu_level=2)
    user_id = message.from_user.id
    await message.answer(text='Fanlardan birini tanlang', reply_markup=get_subjects_kb(user_id))


@dp.message_handler(Text(equals='✔ Imtihon javoblari'))
async def exam_result(message: types.Message):
    await message.answer(text='Siz imtihon javoblariga kirdingiz')


@dp.message_handler(Text(equals="➡ Ko'proq"))
async def more_kb(message: types.Message):
    await message.answer(text="Bu bo'limda siz profilni o'zgartirish, fanlarni tanlash va texnik yordamni foydalanishingiz mumkin",
                         reply_markup=extra_kb)


@dp.message_handler(Text(equals='⬅ Orqaga'))
async def exam_start(message: types.Message, state:FSMContext):
    level = await state.get_data()
    level = level['menu_level'] if 'menu_level' in level else 2
    
    if level in [1,2]:
        await message.answer(text='Asosiy menyu', reply_markup=main_kb)
    elif level == 3:
        print('3')