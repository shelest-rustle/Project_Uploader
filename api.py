import requests
import logging
import json

import config

response = ""

def get_token():
    logging.info(' Функция get_token')
    headers = {
        'Authorization': f'Basic {config.cred}'
    }
    response = requests.request('POST', config.URL_AUTH, headers=headers)
    token = response.json()['token']
    return token


def send_data(url, res):
    logging.info(' Попали в send_data')
    payload = json.dumps(res)
    headers = {
     'Authorization': f'Bearer {get_token()}',
     'Content-Type': 'application/json',
    }
    global response
    response = requests.request('POST', url, headers=headers, data=payload)
    logging.info(f' Отправили запрос: {response}')
    logging.info(f' Тело ответа: {response.json()}')
