from tkinter import Tk, Label, Entry, Button
from tkinter import filedialog as fd
from dotenv import load_dotenv
import logging
import pandas
import json
import re
import requests
import os
from base64 import b64encode
import datetime as dt


load_dotenv()


CRED = os.environ.get('CRED')
URL_AUTH = os.environ.get('URL_AUTH')
URL_PRECOLLECT_TEST = os.environ.get('URL_PRECOLLECT_TEST')
URL_CALLBACK_TEST = os.environ.get('URL_CALLBACK_TEST')
URL_COLLECT_1_TEST = os.environ.get('URL_COLLECT_1_TEST')
URL_COLLECT_2_TEST = os.environ.get('URL_COLLECT_2_TEST')


NAMES = {
    '0': 'преколлекты',
    '1': 'коллект 1',
    '2': 'коллект 2'
}


logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    filename='autom_log'
)


encoded_cred = CRED.encode('ascii')
cred_base64 = b64encode(encoded_cred)
cred = cred_base64.decode('ascii')


def get_token():
    logging.info(' Функция get_token')
    headers = {
        'Authorization': f'Basic {cred}'
    }
    response = requests.request('POST', URL_AUTH, headers=headers)
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


def analitycs(filename):

    logging.info(' Попали в analitycs')
    df = pandas.read_excel(filename)
    logging.info(' Прочитали Excel файл')
    series = str(df['date_payment'])
    clear_date = '.'.join(list(reversed(
        re.search(r'\d{4}-\d{2}-\d{2}', series).group().split('-')
    )))
    df['date_payment'] = clear_date
    df['sum_of_money'] = df['sum_of_money'].astype(str)
    logging.info(' Преобразовали дату и сумму в строку')
    if res == '0':
        logging.info(' Загрузка преколлектов')
        df['list'] = df['list'].astype(str)
        logging.info(' Преобразовали list в строку')
        if df['list'].isin(['0']).any():
            precollect = df[df['list'] == '0']
            logging.info(' Разделили precollect')
            precollect.drop('list', axis=1)
            logging.info(' Убрали колонку list из precollect')
            precollect.to_json('precollect.json', orient='records')
            logging.info(' Создали precollect.json')
            with open('precollect.json', 'r') as f:
                json_data = json.load(f)
            send_data(URL_PRECOLLECT_TEST, json_data)
            logging.info(' Преколлект успешно загружен.')
            os.remove('precollect.json')
            ending()
        else:
            logging.info(' Преколлект не загружен.'
                         ' В колонке list отсутствует 0.')

        if df['list'].isin(list(map(str, range(1, 10)))).any():
            callback = df[df['list'] != '0']
            logging.info(' Разделили callback')
            callback.to_json('precollect_callback.json', orient='records')
            logging.info(' Создали callback.json')
            with open('precollect_callback.json', 'r') as f:
                json_data = json.load(f)
            send_data(URL_CALLBACK_TEST, json_data)
            logging.info(' Преколлект колбэк успешно загружен.')
            os.remove('precollect_callback.json')
            ending()
        else:
            logging.info(' Преколлект колбэк не загружен.'
                         ' В колонке list отсутствуют цифры кроме 0.')
    if res == '1':
        logging.info(' Загрузка первого коллекта')
        collect_1 = df
        collect_1.to_json('collect_1.json', orient='records')
        logging.info(' Создали collect_1.json')
        with open('collect_1.json', 'r') as f:
            json_data = json.load(f)
        send_data(URL_COLLECT_1_TEST, json_data)
        logging.info(' Коллект 1 успешно загружен.')
        os.remove('collect_1.json')
        ending()
    if res == '2':
        logging.info(' Загрузка второго коллекта')
        collect_2 = df
        collect_2.dropna()
        collect_2.drop('upload status', axis=1)
        collect_2.rename(columns={'timezone4': 'timezone'})
        collect_2.to_json('collect_2.json', orient='records')
        logging.info(' Создали collect_2.json')
        with open('collect_2.json', 'r') as f:
            json_data = json.load(f)
        send_data(URL_COLLECT_2_TEST, json_data)
        logging.info(' Коллект 2 успешно загружен.')
        os.remove('collect_2.json')
        ending()


def clicked():

    try:
        global res
        res = str(txt.get())
        if res in ['0', '1', '2']:
            file_name = fd.askopenfilename()
            clear_date = '.'.join(list(reversed(
                str(dt.datetime.today().date()).split('-')
            )))
            logging.info(f' Дата загрузки: {clear_date}')
            logging.info(f' Был передан файл. Путь: {file_name}')
            analitycs(file_name)
        else:
            lbl_error = Label(window,
                              text='Неверный ввод',
                              font=('Arial Bold', 10))
            lbl_error.grid(column=3, row=3, pady=5)
    except FileNotFoundError as e:
        logging.error(f' Файл не найден: {e}')
        return


def ask_open_file():
    global window
    window = Tk()
    window.title('Expo Uploader')
    window.geometry('420x400')
    lbl_main = Label(window, text='Введите 0 для загрузки преколлектов\n'
                     'Введите 1 для загрузки коллекта 1\n'
                     'Введите 2 для загрузки коллекта 2',
                     font=('Arial Bold', 10))
    lbl_main.grid(column=3, row=1, padx=20, pady=20, sticky='n')
    global txt
    txt = Entry(window, width=10)
    txt.grid(column=3, row=4, pady=10)
    txt.focus()
    btn = Button(window, text='Загрузить', command=clicked)
    btn.grid(column=3, row=6)
    window.mainloop()


def ending():
    lbl_fin = Label(window, text=f'Загружено: {NAMES[res]}\n'
                    f'Ответ: {response}\n'
                    'Если код ответа равен 202/200, то загрузка прошла успешно.\n'
                    'Если код отличается, то необходимо передать разработчику\n'
                    'файл autom_log для прояснения ситуации.\n'
                    'Файл autom_log находится в той же директории, что и программа.')
    lbl_fin.grid(column=3, row=10, padx=20, pady=20, sticky='s')


ask_open_file()
