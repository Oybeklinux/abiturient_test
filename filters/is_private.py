from aiogram.types import ChatType, Message
from aiogram.dispatcher.filters import BoundFilter

from data.config import admins


class IsPrivate(BoundFilter):

    async def check(self, message: Message) -> bool:
        return ChatType.PRIVATE == message.chat.type


class IsAdmin(BoundFilter):

    async def check(self, message: Message) -> bool:
        print("message.from_user.id in admins", message.from_user.id in admins)
        return message.from_user.id in admins

