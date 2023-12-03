from aiogram.dispatcher.filters import Filter
from aiogram.types import Message

from loader import db


class IsSubject(Filter):

    subjects = None

    def __init__(self) -> None:
        if not IsSubject.subjects:
            IsSubject.subjects = [f"📚 {row[1]}" for row in db.select_subjects()]

    async def check(self, message: Message):
        # check if text is in the list
        return message.text in IsSubject.subjects
