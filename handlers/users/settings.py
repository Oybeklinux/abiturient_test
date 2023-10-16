from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ContentType

from handlers.users.start import send_user_info
from keyboards import contact_kb
from keyboards.inline.regions import get_region_ikb
from keyboards.inline.settings import settings_ikb, settings_cb
from loader import dp, db
from states.settings import EditState


@dp.message_handler(Text(equals="✏️Profilni o'zgartirish"))
async def profile_edit(message: types.Message):
    await send_user_info(chat_id=message.chat.id, user_id=message.from_user.id)
    # user_id = message.from_user.id
    # user = db.select_user(id=user_id)
    # universitet = user[4] if user[4] else 'Ko\'rsatilmagan'
    # text = (f"Quyida sizning ma'lumorlaringiz keltirilgan:\n\n"
    #         f"*Ismingiz*: {user[1]}\n"
    #         f"*Telefoningiz*: {user[2]}\n"
    #         f"*Viloyatingiz*: {user[3]}\n"
    #         f"*Universitetingiz*: {universitet}\n\n"
    #         f"❗️Ma'lumotlarni quyidagi tugmalar orqali o'zgartiring")
    #
    # await message.answer(text=text, parse_mode=ParseMode.MARKDOWN,
    #                           reply_markup=settings_ikb)


@dp.callback_query_handler(settings_cb.filter(menu='name'))
async def edit_name(call: types.CallbackQuery):
    await call.answer('')
    await call.message.answer(text="To'liq ismingizni kiriting")
    await EditState.FIO.set()


@dp.message_handler(state=EditState.FIO)
async def update_name(message: types.Message, state:FSMContext):
    name = message.text
    user_id = message.from_user.id
    db.update_user(id=user_id, name=name)
    await send_user_info(chat_id=message.chat.id, user_id=message.from_user.id)
    await state.finish()


@dp.callback_query_handler(settings_cb.filter(menu='phone'))
async def edit_phone(call: types.CallbackQuery):
    await call.message.answer(text="Telefon raqamingizni yuboring", reply_markup=contact_kb)
    await EditState.Telefon.set()


@dp.message_handler(content_types=ContentType.CONTACT, state=EditState.Telefon)
async def save_contact(message: types.Message, state:FSMContext):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    db.update_user(id=user_id, phone=phone_number)
    await send_user_info(chat_id=message.chat.id, user_id=message.from_user.id)
    await state.finish()


@dp.callback_query_handler(settings_cb.filter(menu='region'))
async def edit_region(call: types.CallbackQuery):
    await call.message.answer("Viloyatingizni tanlang", reply_markup=get_region_ikb())

# regionni saqlash uchun start.py faylidagi save_region funksiyasi ishga tushadi

@dp.callback_query_handler(settings_cb.filter(menu='university'))
async def edit_university(call: types.CallbackQuery):
    pass
