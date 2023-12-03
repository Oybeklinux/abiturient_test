from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode

from filters.is_private import IsAdmin
from handlers.users.uploader import message_upload, ALLOWED_CONTENT_TYPES
from keyboards.inline.subjects import get_test_subject_ikb, test_subject_cb
from keyboards.inline.tests import test_cb, get_test_ikb
from loader import dp, bot, db
from utils.misc.exam_question import generate_question


# when user sends insert_test command
@dp.message_handler(Command('insert_test'), IsAdmin())
async def select_subject_for_test(message: types.Message):
    await message.answer(text="Testni qaysi fandan kiritmoqchisiz", reply_markup=get_test_subject_ikb())


# when users selects one of subjects
@dp.callback_query_handler(test_subject_cb.filter(), IsAdmin())
async def insert_test(call: types.CallbackQuery, state: FSMContext):
    data = test_subject_cb.parse(call.data)
    state_data = get_empty_data()

    state_data['subject_id'] = data['id']
    subject_name = data['name']
    await state.update_data(**state_data)

    await call.message.edit_text(
        text=f"<b>{subject_name.title()}</b> fanidan test kiritish uchun savol va javoblarni tanlab matn, audio, video,fayl ko'rinishida "
             "jo'nitishingiz mumkin", reply_markup=get_test_ikb(state_data), parse_mode=ParseMode.HTML)


# when user select write answer
@dp.callback_query_handler(test_cb.filter(mtype='answer'))
async def tick_answer(call: types.CallbackQuery, state: FSMContext):
    cb_data = test_cb.parse(call.data)
    correct_answer = cb_data['what']
    state_data = await state.get_data()

    state_data[correct_answer]['correct'] = not state_data[correct_answer]['correct']

    await state.update_data(**state_data)
    await edit_question(message=call.message, data=state_data)


# when user clicks save button
@dp.callback_query_handler(test_cb.filter(what='s'))
async def save_answer_and_question(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        assert data['q']['text']
        assert data['a1']['text']
        assert data['a2']['text']
    except:
        await call.answer(text="Kamida savol va ikkita javob bo'lishi kerak")
        return
    try:
        assert data['subject_id']
    except:
        await call.answer(text="Fan noma'lum. Fanni tanlash kerak")
        return
    db.insert_test(data)
    await call.answer('Saqlandi')
    await state.reset_state()
    await call.message.delete()


# when user clicks back button
@dp.callback_query_handler(test_cb.filter(what='back'), IsAdmin())
async def back_2_test_subjects(call: types.CallbackQuery):
    await call.message.edit_text(text="Testni qaysi fandan kiritmoqchisiz", reply_markup=get_test_subject_ikb())


# when user clicks question or one of answers
@dp.callback_query_handler(test_cb.filter())
async def insert_option_clicked(call: types.CallbackQuery, state: FSMContext):
    inline_data = test_cb.parse(call.data)
    media_types = {'text': 'matnini', "audio": "audiosini", "video": "videosini", "image": "rasmini", "file": "faylini"}
    m_type = media_types[inline_data['mtype']]

    what = "Savol" if inline_data['what'] == 'q' else f"Javob {inline_data['what'][1]}"

    state_data = await state.get_data()

    state_data['message_id'] = call.message.message_id
    state_data['what'] = inline_data['what']
    state_data['mtype'] = inline_data['mtype']

    await state.update_data(**state_data)
    await state.set_state('test_insert')
    await call.answer(text=f"{what}ning {m_type} jo'nating", show_alert=True)


# when user sends text
@dp.message_handler(state='test_insert', content_types=types.ContentType.TEXT)
async def test_text_inserted(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    what = state_data['what']  # question/answer1/answer2 ...
    m_type = state_data['mtype']  # text
    text = message.html_text

    # save inserted date to state
    state_data[what][m_type] = text

    # state ma'lumotini yangilash
    await state.update_data(**state_data)
    await message.delete()
    await edit_question(message, state_data)
    await state.reset_state(with_data=False)


# when user sends photo
@dp.message_handler(state='test_insert', content_types=ALLOWED_CONTENT_TYPES)
async def test_photo_inserted(message: types.Message, state: FSMContext):
    data = await state.get_data()
    what = data['what']  # question/answer1/answer2 ...
    mtype = data['mtype']  # text/audio/video ...

    url = await message_upload(message, state)
    data[what][mtype] = url
    await state.update_data(**data)
    await message.delete()
    await edit_question(message, data)
    await state.reset_state(with_data=False)


# CODE OPTIMIZATION

def get_empty_data():
    """
    data structure of test
    :return: dict
    """
    question = {'text': None, 'image': None, 'video': None, 'file': None, 'audio': None}
    answer = question.copy()
    answer['correct'] = False

    return {
        'q': question, 'a1': answer.copy(), 'a2': answer.copy(), 'a3': answer.copy(), 'a4': answer.copy(),
        'subject_id': None, 'message_id': None,
        'what': None, 'mtype': None
    }


async def edit_question(message: types.Message, data):
    """
    edits the question when question/answer/buttons changes
    :param message: - which is going to be changed
    :param data: - which we need to generate inline buttons
    :return: None
    """
    content = await generate_question(data)

    message_id = data['message_id']

    await bot.edit_message_text(text=content, chat_id=message.chat.id,
                                message_id=message_id,
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_test_ikb(data))


async def delete_message(chat_id, message_id):
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


