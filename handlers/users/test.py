import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.is_in import IsIn
from loader import dp, db


@dp.message_handler(IsIn())
async def show_subject_exam(message: types.Message, state:FSMContext):
    subject = message.text.replace('📚','').strip()
    subject_id = db.select_subject_id(subject)

    tests = db.select_tests(subject_id)
    if not tests:
        return await message.answer("Kechirasiz bu fandan hali test kiritilmagan")

    test = random.choice(tests)
    await state.update_data(subject=subject_id, tests_done="")
    await message.answer(text=f"{test[0]}\n{test[1]}")


