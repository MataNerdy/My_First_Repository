from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types import Message

BOT_TOKEN = ''
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

admin_ids: list[int] = []

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    print(message.from_user.id, message.text)
    await message.answer(text='Приветствую, админ!')

@dp.message()
async def answer_if_not_admins_update(message: Message):
    print(message.from_user.id, message.text)
    await message.answer(text='Вы не админ')

if __name__ == "__main__":
    dp.run_polling(bot)