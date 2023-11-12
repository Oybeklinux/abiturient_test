from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

test_cb = CallbackData('tests_menu', 'what', 'mtype')


def get_test_ikb2():
    inline_keyboard = []
    item_types = {'text': f"🖊 #text", 'image': "📸", 'audio': "🎙", 'video': "🎥", 'file': "📄"}
    for what_ in ['q', 'a1', 'a2', 'a3', 'a4']:
        keyboard_buttons = []
        text = what_.replace('a', 'Javob ').replace('q', 'Savol')
        for type_, label in item_types.items():
            label = label.replace('#text', text)
            keyboard_buttons.append(
                InlineKeyboardButton(text=label, callback_data=test_cb.new(what=what_, mtype=type_))
            )
        inline_keyboard.append(keyboard_buttons)
    inline_keyboard.append([
        InlineKeyboardButton(text="💾 Saqlash", callback_data=test_cb.new(what='s', mtype='')),
        InlineKeyboardButton(text="⬅️Orqaga", callback_data=test_cb.new(what='back', mtype=''))
    ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_answer_sign(data, which_answer):

    try:
        if data[which_answer]['correct']:
            return '✅'
    except:
        pass
    return ''


def get_test_ikb(data=None):
    a1 = get_answer_sign(data, 'a1') + " A"
    a2 = get_answer_sign(data, 'a2') + " B"
    a3 = get_answer_sign(data, 'a3') + " C"
    a4 = get_answer_sign(data, 'a4') + " D"
    print("data:", data)
    print("a1:", a1)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=a1, callback_data=test_cb.new(what='a1', mtype='answer')),
                InlineKeyboardButton(text=a2, callback_data=test_cb.new(what='a2', mtype='answer')),
                InlineKeyboardButton(text=a3, callback_data=test_cb.new(what='a3', mtype='answer')),
                InlineKeyboardButton(text=a4, callback_data=test_cb.new(what='a4', mtype='answer')),
            ],
            [
                InlineKeyboardButton(text="🖊 Savol matni", callback_data=test_cb.new(what='q', mtype='text')),
                InlineKeyboardButton(text="📸 Rasm", callback_data=test_cb.new(what='q', mtype='image')),
                # InlineKeyboardButton(text="🎙", callback_data=test_cb.new(what='q', mtype='audio')),
                InlineKeyboardButton(text="🎥 Video", callback_data=test_cb.new(what='q', mtype='video')),
                # InlineKeyboardButton(text="📄", callback_data=test_cb.new(what='q', mtype='file')),
            ],
            [
                InlineKeyboardButton(text="🖊 Javob1 matni", callback_data=test_cb.new(what='a1', mtype='text')),
                InlineKeyboardButton(text="🖊 Javob2 matni", callback_data=test_cb.new(what='a2', mtype='text')),
                InlineKeyboardButton(text="🖊 Javob3 matni", callback_data=test_cb.new(what='a3', mtype='text')),
                InlineKeyboardButton(text="🖊 Javob4 matni", callback_data=test_cb.new(what='a4', mtype='text')),
            ],
            [
                InlineKeyboardButton(text="💾 Saqlash", callback_data=test_cb.new(what='s', mtype='')),
                InlineKeyboardButton(text="⬅️Orqaga", callback_data=test_cb.new(what='back', mtype=''))
            ]
            # [
            #     InlineKeyboardButton(text="🖊 Javob1 matni", callback_data=test_cb.new(what='a1', mtype='text')),
            # InlineKeyboardButton(text="📸", callback_data=test_cb.new(what='a1', mtype='image')),
            # InlineKeyboardButton(text="🎙", callback_data=test_cb.new(what='a1', mtype='audio')),
            # InlineKeyboardButton(text="🎥", callback_data=test_cb.new(what='a1', mtype='video')),
            # InlineKeyboardButton(text="📄", callback_data=test_cb.new(what='a1', mtype='file')),
            # ],
            # [
            #     InlineKeyboardButton(text="🖊 Javob2 matni", callback_data=test_cb.new(what='a2', mtype='text')),
            # InlineKeyboardButton(text="📸", callback_data=test_cb.new(what='a2', mtype='image')),
            # InlineKeyboardButton(text="🎙", callback_data=test_cb.new(what='a2', mtype='audio')),
            # InlineKeyboardButton(text="🎥", callback_data=test_cb.new(what='a2', mtype='video')),
            # InlineKeyboardButton(text="📄", callback_data=test_cb.new(what='a2', mtype='file')),
            # ],
            # [
            #     InlineKeyboardButton(text="🖊 Javob3 matni", callback_data=test_cb.new(what='a3', mtype='text')),
            # InlineKeyboardButton(text="📸", callback_data=test_cb.new(what='a3', mtype='image')),
            # InlineKeyboardButton(text="🎙", callback_data=test_cb.new(what='a3', mtype='audio')),
            # InlineKeyboardButton(text="🎥", callback_data=test_cb.new(what='a3', mtype='video')),
            # InlineKeyboardButton(text="📄", callback_data=test_cb.new(what='a3', mtype='file')),
            # ],
            # [
            #     InlineKeyboardButton(text="🖊 Javob4 matni", callback_data=test_cb.new(what='a4', mtype='text')),
            # InlineKeyboardButton(text="📸", callback_data=test_cb.new(what='a4', mtype='image')),
            # InlineKeyboardButton(text="🎙", callback_data=test_cb.new(what='a4', mtype='audio')),
            # InlineKeyboardButton(text="🎥", callback_data=test_cb.new(what='a4', mtype='video')),
            # InlineKeyboardButton(text="📄", callback_data=test_cb.new(what='a4', mtype='file')),
            # ],
            # [
            #     InlineKeyboardButton(text="💾Saqlash", callback_data=test_cb.new(what='s', mtype='')),
            # ]
        ],
    )
