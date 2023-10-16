import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType, ReplyKeyboardRemove, ParseMode
from keyboards import contact_kb
from keyboards.default.main import main_kb
from keyboards.default.register import register_kb, register2_kb
from keyboards.inline.regions import region_cb, get_region_ikb
from keyboards.inline.settings import settings_cb, settings_ikb
from loader import dp, db, bot
from states.register_state import RegisterState


@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    try:
        db.add_user(id=user_id, name=message.from_user.full_name)
    except sqlite3.IntegrityError:
        pass

    text = f"Assalomu alaykum, {message.from_user.full_name}.\"Kelajagim\" botiga hush kelibsiz. Shu yerdan o'z kelajagingizga ilk qadamni tashlaysiz. \n*Alloh omadingizni bersin!*"
    user = db.select_user(id=user_id)
    if user[6]:
        await message.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=main_kb)
    elif user[2]:
        await message.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=register2_kb)
    else:
        await message.answer(text, reply_markup=register_kb, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(text="✅ Ro'yxatdan o'tish")
async def register(message: types.Message):
    await message.answer("Ro'yxatdan o'tish uchun telefon raqamingizni yuboring", reply_markup=contact_kb)
    await RegisterState.Telefon.set()


@dp.message_handler(content_types=ContentType.CONTACT, state=RegisterState.Telefon)
async def save_contact(message: types.Message, state:FSMContext):
    contact = message.contact
    phone_number = contact.phone_number

    user_id = message.from_user.id

    if db.is_user_registered(user_id):
        await message.answer(text="Telefon raqamingiz muvaffaqiyarli o'zgartirildi", reply_markup=get_settings_kb())
        await state.finish()
    else:
        await message.answer(text="Ism, sharifingiz va otangizni ismini bittada kiriting", reply_markup=ReplyKeyboardRemove())
        await RegisterState.FIO.set()
    db.update_user(id=user_id, phone=phone_number)


@dp.message_handler(state=RegisterState.FIO)
async def save_name(message: types.Message, state: FSMContext):
    await message.answer("Viloyatingizni tanlang", reply_markup=get_region_ikb())

    user_id = message.from_user.id
    db.update_user(id=user_id, name=message.text)
    await state.finish()


@dp.callback_query_handler(region_cb.filter())
async def save_region(call: types.CallbackQuery):
    region = region_cb.parse(call.data)['region']
    db.update_user(id=call.from_user.id, region_id=region)
    await call.answer('')
    await send_user_info(chat_id=call.message.chat.id, user_id=call.from_user.id)


async def send_user_info(chat_id, user_id):
    user = db.select_user(id=user_id)
    universitet = user[4] if user[4] else 'Ko\'rsatilmagan'

    await bot.send_message(chat_id=chat_id, text='Ma\'lumotlaringiz: ', parse_mode=ParseMode.MARKDOWN,
                           reply_markup=register2_kb)
    text = (f"*Ismingiz*: {user[1]}\n"
            f"*Telefoningiz*: {user[2]}\n"
            f"*Viloyatingiz*: {user[3]}\n"
            f"*Universitetingiz*: {universitet}\n\n"
            f"❗️Ma'lumotlarni quyidagi tugmalar orqali o'zgartiring")

    await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=settings_ikb)












