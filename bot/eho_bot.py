from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = ''

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer('Приветствую тебя, я бот-эхо!\nНапиши мне что-нибудь, и я повторю это!')

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('Я бот-эхо, и я повторяю все, что ты мне напишешь!\nПросто напиши мне что-нибудь, и я повторю это!')

@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)

if __name__ == '__main__':
    dp.run_polling(bot)
