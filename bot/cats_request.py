import requests
import time

API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '8344205366:AAG_8JoYVArQ-YUtSq2XHGKDnvpdWy_ds-c'
ERROR_MESSAGE = 'Кошечка не нашлась :('

offset = -2
counter = 0
MAX_COUNTER = 100
cat_responce: requests.Response
cat_link: str

while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']

            cat_responce = requests.get(API_CATS_URL)
            if cat_responce.status_code == 200:
                cat_link = cat_responce.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_MESSAGE}')

    time.sleep(1)
    counter += 1