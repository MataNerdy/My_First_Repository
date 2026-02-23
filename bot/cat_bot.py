from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import requests

BOT_TOKEN = ''
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
ERROR_MESSAGE = 'Кошечка не нашлась :('
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer('Приветствую тебя, я бот, который может отправлять тебе столько картинок с котиками, сколько ты захочешь!\nНапиши мне что-нибудь, и я пришлю тебе кота :)')

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('Я бот, который может отправлять тебе котиков в неограниченном количестве!\nПросто напиши мне что-нибудь, и я пришлю тебе котика!')

@dp.message()
async def send_echo(message: Message):
    cat_responce = requests.get(API_CATS_URL)
    if cat_responce.status_code == 200:
        cat_link = cat_responce.json()[0]['url']
        await message.answer_photo(photo=cat_link)
    else:
        await message.reply(text=ERROR_MESSAGE)

if __name__ == '__main__':
    dp.run_polling(bot)