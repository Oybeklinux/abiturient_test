from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default.main import main_kb
from keyboards.default.register import select_subject_confirm_kb
from keyboards.inline.subjects import get_subject_ikb, subject_cb
from loader import dp, db


@dp.message_handler(Text(equals="✔ Fanlarni tanlash"))
async def select_subjects(message: types.Message, state:FSMContext):
    user_id=message.from_user.id
    text = f"Majburiy fanlar\n"
    rows = db.select_subjects(is_main=True)
    main_subjects = [f'\t- {row[1]}' for row in rows]
    text += '\n'.join(main_subjects)
    data = await state.get_data()
    level = data['menu_level'] if data and 'menu_level' in data else None
    if level is None:
        await message.answer(text=text, reply_markup=select_subject_confirm_kb)
    await message.answer(text="Qo'shimcha 2 fanlarni tanlang:", reply_markup=get_subject_ikb(user_id=user_id))


@dp.callback_query_handler(subject_cb.filter())
async def select_subject(call:types.CallbackQuery):
    subject_id = int(subject_cb.parse(call.data)['subject'])
    user_id = call.from_user.id
    user_subjects = db.select_2_subjects(user_id)
    print(user_subjects[1], subject_id)
    print(type(user_subjects[1]), type(subject_id))

    if user_subjects[1] == subject_id:
        db.update_user(id=user_id, subject2=None)
        await call.message.edit_reply_markup(reply_markup=get_subject_ikb(user_id))
    elif user_subjects[0] == subject_id:
        db.update_user(id=user_id, subject1=None)
        await call.message.edit_reply_markup(reply_markup=get_subject_ikb(user_id))
    else:

        if user_subjects[1] and user_subjects[0]:
            text = "Siz faqat ikkita fanni tanlashingiz mumkin"
            await call.answer(text=text, show_alert=True, cache_time=1)
        elif not user_subjects[0]:
            db.update_user(id=user_id, subject1=subject_id)
            await call.message.edit_reply_markup(reply_markup=get_subject_ikb(user_id))
        elif not user_subjects[1]:
            db.update_user(id=user_id, subject2=subject_id)
            await call.message.edit_reply_markup(reply_markup=get_subject_ikb(user_id))
        else:
            raise Exception("Ko'rilmagan holar")
            # db.update_user(id=user_id, subject1=subject_id)
            # await call.message.edit_reply_markup(reply_markup=get_subject_ikb(user_id))


@dp.message_handler(Text(equals="✅ Tasdiqlash"))
async def select_subjects_confirm(message: types.Message):
    await message.answer(text="Siz ro'yxatdan muvaffaqiyatli o'tdingiz", reply_markup=main_kb)