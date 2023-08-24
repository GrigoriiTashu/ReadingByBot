import random
import requests
import time


API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = '11111'
# TEXT: str = input()
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
chat_id: int

while counter < MAX_COUNTER:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:

        for result in updates['result']:
            print(result['message']['text'])
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={input()}')

    time.sleep(1)
    counter += 1
