from datetime import datetime
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from keyboards.default.exam import get_subjects_kb
from keyboards.default.main import extra_kb, main_kb
from keyboards.inline.tests import get_exam_list_ikb, exam_list_cb
from loader import dp, db


@dp.message_handler(Text(equals='🧑‍💻 Test imtihoni'))
async def exam_start(message: types.Message, state: FSMContext):
    await state.update_data(menu_level=2)
    user_id = message.from_user.id
    await message.answer(text='Fanlardan birini tanlang', reply_markup=get_subjects_kb(user_id))


@dp.message_handler(Text(equals='✔ Imtihon javoblari'))
async def exam_result(message: types.Message):
    content = f"Imtihonlardan birini tanlang:\n"
    await message.answer(text=content, reply_markup=get_exam_list_ikb())


@dp.callback_query_handler(exam_list_cb.filter())
async def exam_selected(call: types.CallbackQuery):
    data = exam_list_cb.parse(call.data)
    exam_id = data['exam_id']
    start_date = data['start_date'].replace('_', ':')
    print(exam_id, start_date)
    await send_exam_report(call.message, exam_id, start_date)
    await call.answer(text='', cache_time=0)


@dp.message_handler(Text(equals="➡ Ko'proq"))
async def more_kb(message: types.Message):
    await message.answer(
        text="Bu bo'limda siz profilni o'zgartirish, fanlarni tanlash va texnik yordamni foydalanishingiz mumkin",
        reply_markup=extra_kb)


@dp.message_handler(Text(equals='⬅ Orqaga'))
async def exam_start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'start_time' in data:
        exam_id = data['exam_id']
        db.save_exam_report(exam_id)
        await send_exam_report(message, exam_id, data['start_time'])
        await state.finish()

    await message.answer(text='Asosiy menyu', reply_markup=main_kb)
    # hozircha bu kod kerak emas
    # level = await state.get_data()
    # level = level['menu_level'] if 'menu_level' in level else 2
    #
    # if level in [1,2]:
    #     await message.answer(text='Asosiy menyu', reply_markup=main_kb)
    # elif level == 3:
    #     print('3')


async def send_exam_report(message: types.Message, exam_id, start_datetime: Union[str, datetime]):
    rows = db.select_exam_report(exam_id)
    print(rows)
    if type(start_datetime) is datetime:
        start_datetime = start_datetime.strftime("%d-%m-%Y %H:%M:%S")
    dt, tm = start_datetime.split()

    content = f'*{dt}* sana *{tm}* vaqtdagi *test imtihon natijalari*:\n\n*Jami*: #total\n\n'
    total_point = 0
    if not rows:
        await message.answer(text="Ma'lumot topilmadi", parse_mode=ParseMode.MARKDOWN)
        return
    for row in rows:
        total_point += row[4]
        content += f"*{row[2]}*: {row[4]}\n\t✅ {row[6]} ta, " \
                   f"❌ {row[7]} ta, ⭕ {row[8]} \n\n"

    content = content.strip().replace("#total", str(total_point))
    await message.answer(text=content, parse_mode=ParseMode.MARKDOWN)
