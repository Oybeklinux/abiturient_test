from aiogram import types
from loader import dp

# Главное -> Курсы 💻 -> Поиск
@dp.inline_handler(text='')
async def search(query: types.InlineQuery):
    search_word = query.query or ''

    results = [types.InlineQueryResultArticle(
        id='1',
        title='Python и Django',
        thumb_url='https://telegra.ph/file/1ed2732d276af0a239ca1.png',
        description='Основы программирования. ООП. GUI приложений. Создание веб-приложений',
        input_message_content=types.InputTextMessageContent(
            message_text='course_Python#'
        )
    ),
        types.InlineQueryResultArticle(
            id='2',
            title='Flutter. Dart',
            thumb_url='https://telegra.ph/file/7aa34eeab125b70322d44.png',
            description='Разработка приложений под различные операционные системы',
            input_message_content=types.InputTextMessageContent(
                message_text='course_Flutter#'
            )
        ),
        types.InlineQueryResultArticle(
            id='3',
            title='Php',
            thumb_url='https://telegra.ph/file/62bb42714b939611154db.png',
            description='Разработка веб-приложений на языке php',
            input_message_content=types.InputTextMessageContent(
                message_text='course_Php#'
            )
        )
    ]
    await query.answer(results, cache_time=1, is_personal=True)