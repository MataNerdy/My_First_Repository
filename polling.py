import requests
import time

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '8344205366:AAG_8JoYVArQ-YUtSq2XHGKDnvpdWy_ds-c'
offset = -2
timeout = 60
updates: dict

def do_something() -> None:
    print('Был апдейт...')
counter = 0
MAX_COUNTER = 100
while counter < MAX_COUNTER:
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            do_something()

    end_time = time.time()
    print(f'Время между запросами к Telegram Bot Api: {end_time - start_time} с')
    counter += 1