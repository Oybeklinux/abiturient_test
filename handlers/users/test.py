import datetime
import json
import random
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from filters.is_in import IsSubject
from keyboards.default.exam import get_subjects_kb

from keyboards.default.test_kb import get_tests_kb
from keyboards.inline.tests import get_question_options, test_answer_cb
from loader import dp, db, bot
from utils.misc.exam_question import generate_question


# when users clicks back button to switch to subject selection menu
@dp.message_handler(text='⬅ Orqaga', state="exam_state")
async def back_to_subjects(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message1_id = data['message1_id']
    chat_id = data['chat_id']
    message2_id = data['message2_id']
    # await bot.delete_message(chat_id=chat_id, message_id=message1_id)
    # await bot.delete_message(chat_id=chat_id, message_id=message2_id)
    saving_data = {
        'start_time': data['start_time'],
        'exam_id': data['exam_id']
    }
    await state.set_data(saving_data)
    await state.reset_state(with_data=False)
    user_id = message.from_user.id
    await message.answer(text="✔ Fanlarni tanlash", reply_markup=get_subjects_kb(user_id))


# when user selects one of subjects
@dp.message_handler(IsSubject())
async def show_subject_exam(message: types.Message, state: FSMContext):
    subject = message.text.replace('📚', '').strip()
    subject_id = db.select_subject_id(subject)
    data = await state.get_data()

    # create exam_id if it is first test to take exam
    exam_id = db.begin_exam() if 'exam_id' not in data else data['exam_id']

    tests = db.select_tests(subject_id)
    if not tests:
        return await message.answer("Kechirasiz bu fandan hali test kiritilmagan")

    random.shuffle(tests)
    i = 0
    questions = {}
    for row in tests:
        questions[row[0]] = await get_right_answer(row)
        i += 1

    # when stars exam first time save the start time
    if not data or "start_time" not in data:
        data = {"start_time": datetime.datetime.now()}

    # selected subject id, get all question id, right answer and exam id
    data['subject_id'] = subject_id
    data['subject'] = subject
    data['questions'] = questions  # all question id and right answer: a1/a2/a3/a4
    data['answered'] = {}  # test id: ['a1','a2],
    data['exam_id'] = exam_id

    await state.set_data(data)
    mes1_id, chat_id, mes2_id = await send_question(message, state)
    data = await state.get_data()
    data['message1_id'] = mes1_id
    data['chat_id'] = chat_id
    data['message2_id'] = mes2_id
    await state.set_data(data)


async def send_question(message: types.Message, state: FSMContext, test_num=None):
    data = await state.get_data()
    tests = data['questions']

    # if question_num is not given them start from 1st question
    if not test_num:
        test_num = 1

    # get next test id
    current_test_id = list(tests.keys())[test_num - 1]
    # get question and answers of the test
    cur_test = db.select_test(current_test_id)
    # save current test data to state
    data['current'] = cur_test
    # generate the test in specified format
    content = await generate_question(cur_test, False)
    time_left, ended = get_time_left_for_exam(data['start_time'])
    if ended:
        await message.answer(text="Vaqtingiz tugadi")
        return
    content += f"\n⏳ {time_left}"
    # all answered tests id

    # id of all user answered tests
    answered_tests_id = list(data['answered'].keys())
    # user answers of the current test
    cur_test_user_answers = data['answered'][current_test_id] if current_test_id in data['answered'] else []

    # all tests id
    all_tests_id = list(data['questions'].keys())

    await state.set_state('exam_state')
    await state.set_data(data)
    # SEND QUESTION
    # send the test. if it is not first question then edit the previous question
    # send the test. if it is not first question then edit the previous question
    mes2 = None
    if 'message2_id' not in data:
        mes2 = await message.answer(text=content,
                                    reply_markup=get_question_options(cur_test_user_answers),
                                    parse_mode=ParseMode.HTML)
    else:
        chat_id = data['chat_id']
        message2_id = data['message2_id']
        mes2 = await bot.edit_message_text(text=content,
                                    chat_id=chat_id,
                                    message_id=message2_id,
                                    reply_markup=get_question_options(cur_test_user_answers),
                                    parse_mode=ParseMode.HTML)

    if 'message2_id' in data:
        chat_id = data['chat_id']
        message1_id = data['message1_id']
        await bot.delete_message(chat_id=chat_id,
                           message_id=message1_id)
    mes1 = await message.answer(text=f"<b>Savol {test_num}</b>",
                                reply_markup=get_tests_kb(all_tests=all_tests_id,
                                                          answered_tests=answered_tests_id,
                                                          current_test_id=current_test_id),
                                parse_mode=ParseMode.HTML)
    return mes1.message_id, mes1.chat.id, mes2.message_id


# when user sends number or when user clicks question number button
@dp.message_handler(state="exam_state", regexp=r'^[✅📍]?([1-9]|1[0-9]|2[0-9]|3[0-6])$')
async def show_exam_question(message: types.Message, state: FSMContext):
    num = message.text.replace('✅', '').replace('📍', '')

    await message.delete()
    if not re.match(r'^([1-9]|1[0-9]|2[0-9]|3[0-6])$', num):
        return

    await send_question(message, state, int(num))


# when user choose an answer
@dp.callback_query_handler(test_answer_cb.filter(), state='exam_state')
async def user_chose_answer(call: types.CallbackQuery, state: FSMContext):
    cb_data = test_answer_cb.parse(call.data)
    user_answer = cb_data['option']
    data = await state.get_data()

    """if user selects answer then save it as {test_id: ['a1','a2']}"""
    cur_question = data['current']
    if cur_question['id'] not in data['answered']:  # searches from keys
        data['answered'][cur_question['id']] = [user_answer]
    elif user_answer in data['answered'][cur_question['id']]:
        data['answered'][cur_question['id']].remove(user_answer)
    else:
        data['answered'][cur_question['id']].append(user_answer)

    time_left, ended = get_time_left_for_exam(data['start_time'])
    if ended:
        await call.message.answer(text="Vaqtingiz tugadi")
        return

    await state.update_data(data)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=get_question_options(data['answered'][cur_question['id']]))
    db.insert_test_result(data)


# helper functions
# gets the right answers
async def get_right_answer(row):
    a1 = json.loads(row[3])
    a2 = json.loads(row[4])
    a3 = json.loads(row[5])
    a4 = json.loads(row[6])
    answers = []
    if a1['correct']:
        answers.append('a1')
    if a2['correct']:
        answers.append('a2')
    if a3['correct']:
        answers.append('a3')
    if a4['correct']:
        answers.append('a4')
    return answers


# get hh:mm:ss time left
def get_time_left_for_exam(start_time):
    """
    gets time left for the exam in format hh:mm:ss
    params: start_time - start time of exam
    return hh:mm:ss, ended
        hh:mm:ss:str - time
        ended:bool - True if there is no time, False if there is time left for the exam
    """
    exam_time = 60 * 60 * 3
    current_time = datetime.datetime.now()
    diff_in_sec = current_time - start_time
    if diff_in_sec.seconds >= exam_time:
        return None, True
    time_left = exam_time - diff_in_sec.seconds
    hh = time_left // 3600
    time_left = time_left % 3600
    mm = time_left // 60
    ss = time_left % 60
    if hh < 10: hh = f'0{hh}'
    if mm < 10: mm = f'0{mm}'
    if ss < 10: ss = f'0{ss}'

    return f"{hh}:{mm}:{ss}", False


# Agar test bazada yechilgani saqlangan bo'lsa, unda u tanlagan javoblarini ham ko'rsatsin