import asyncio
import io
import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType


from filters import IsPrivate
from utils import delete_message
from utils.misc import edit_message, waiting_previous_execution, rate_limit

from telegraph.api import Telegraph
from telegraph.exceptions import (TelegraphException, RetryAfterError,
                                    FileTypeError, FileEmptyError, FileToBigError)
from loader import dp

ALLOWED_CONTENT_TYPES = [
    ContentType.PHOTO, ContentType.VIDEO, ContentType.VIDEO_NOTE,
    ContentType.VOICE,
    ContentType.DOCUMENT, ContentType.ANIMATION, ContentType.AUDIO
]


@rate_limit(2.2)
@waiting_previous_execution
@dp.message_handler(IsPrivate(), content_types=ALLOWED_CONTENT_TYPES)
async def message_upload(message: Message, state: FSMContext):
    # if message.content_type in ALLOWED_CONTENT_TYPES:
    telegraph = Telegraph()
    file, file_size = io.BytesIO(), 0

    mes = emoji = await message.reply("⌛️")
    await state.update_data(throttling=True)

    try:
        if message.content_type == ContentType.VOICE:
            file = await message.voice.download(destination_file=file)

        if message.content_type == ContentType.AUDIO:
            file = await message.audio.download(destination_file=file)

        if message.content_type == ContentType.PHOTO:
            file = await message.photo[-1].download(destination_file=file)

        elif message.content_type == ContentType.VIDEO:
            file = await message.video.download(destination_file=file)

        elif message.content_type == ContentType.VIDEO_NOTE:
            file = await message.video_note.download(destination_file=file)

        elif message.content_type == ContentType.ANIMATION:
            file = await message.animation.download(destination_file=file)

        elif message.content_type == ContentType.DOCUMENT:
            file = await message.document.download(destination_file=file)

        uploaded = await telegraph.upload_file(file.getbuffer())
        # await edit_message(emoji, uploaded.url, disable_web_page_preview=True)

        await mes.delete()
    except FileToBigError as e:
        await edit_message(emoji, "🤨")
        await asyncio.sleep(2)

        file_size = e.__str__().split(":")[1]
        text = "File is to big"
        await emoji.edit_text(text.format(file_size))

    except RetryAfterError as e:
        await edit_message(emoji, "😴")
        await asyncio.sleep(2)

        seconds = re.match(r"\d+", e.__str__())
        text = "retry_after_error"
        await emoji.edit_text(text.format(seconds))

    except (FileTypeError, FileEmptyError):
        await edit_message(emoji, "🙄")
        await asyncio.sleep(2)

        text = "file_type_error"
        await emoji.edit_text(text)

    except TelegraphException:
        await edit_message(emoji, "❗️")
        await asyncio.sleep(2)

        text = "another_error"
        await emoji.edit_text(text)

    finally:
        await state.update_data(throttling=False)
    return uploaded.url
    # else:
    #     emoji = await message.reply("🙄")
    #     await asyncio.sleep(2)
    #
    #     text = "file_type_error"
    #     await edit_message(emoji, text)
