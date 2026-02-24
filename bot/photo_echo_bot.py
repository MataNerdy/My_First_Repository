from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = '8344205366:AAHDWFxMopRjqqqidWXdGMW3M2wXAMS05mI'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def process_start_command(message: Message):
    await message.answer('Приветствую тебя, я бот-эхо!\nНапиши мне что-нибудь!')

async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь,'
                         'и я повторю это!'
    )
async def sent_photo(message: Message):
    await message.reply_photo(message.photo[0].file_id)

async def send_echo(message: Message):
    await message.reply(text=message.text)

dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(sent_photo, F.photo)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)