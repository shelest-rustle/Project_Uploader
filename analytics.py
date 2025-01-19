import pandas
import logging
import re
import os
import json

import config
import api
import tk_interface


def analytics(filename):

    logging.info(' Попали в analytics')
    df = pandas.read_excel(filename)
    logging.info(' Прочитали Excel файл')
    series = str(df['date_payment'])
    clear_date = '.'.join(list(reversed(
        re.search(r'\d{4}-\d{2}-\d{2}', series).group().split('-')
    )))
    df['date_payment'] = clear_date
    df['sum_of_money'] = df['sum_of_money'].astype(str)
    logging.info(' Преобразовали дату и сумму в строку')
    if tk_interface.res == '0':
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
            api.send_data(config.URL_AGENT1_TEST, json_data)
            logging.info(' Преколлект успешно загружен.')
            os.remove('precollect.json')
            tk_interface.ending()
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
            api.send_data(config.URL_AGENT2_TEST, json_data)
            logging.info(' Преколлект колбэк успешно загружен.')
            os.remove('precollect_callback.json')
            tk_interface.ending()
        else:
            logging.info(' Преколлект колбэк не загружен.'
                         ' В колонке list отсутствуют цифры кроме 0.')
    if tk_interface.res == '1':
        logging.info(' Загрузка первого коллекта')
        collect_1 = df
        collect_1.to_json('collect_1.json', orient='records')
        logging.info(' Создали collect_1.json')
        with open('collect_1.json', 'r') as f:
            json_data = json.load(f)
        api.send_data(config.URL_AGENT3_TEST, json_data)
        logging.info(' Коллект 1 успешно загружен.')
        os.remove('collect_1.json')
        tk_interface.ending()
    if tk_interface.res == '2':
        logging.info(' Загрузка второго коллекта')
        collect_2 = df
        collect_2.dropna()
        collect_2.drop('upload status', axis=1)
        collect_2.rename(columns={'timezone4': 'timezone'})
        collect_2.to_json('collect_2.json', orient='records')
        logging.info(' Создали collect_2.json')
        with open('collect_2.json', 'r') as f:
            json_data = json.load(f)
        api.send_data(config.URL_AGENT4_TEST, json_data)
        logging.info(' Коллект 2 успешно загружен.')
        os.remove('collect_2.json')
        tk_interface.ending()
