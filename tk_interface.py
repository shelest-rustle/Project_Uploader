import datetime as dt
import logging

from tkinter import Tk, Label, Entry, Button
from tkinter import filedialog as fd

import config
import api

from analytics import analytics


res = ""


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
            analytics(file_name)
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
    lbl_fin = Label(window, text=f'Загружено: {config.NAMES[res]}\n'
                    f'Ответ: {api.response}\n'
                    'Если код ответа равен 202/200, то загрузка прошла успешно.\n'
                    'Если код отличается, то необходимо передать разработчику\n'
                    'файл autom_log для прояснения ситуации.\n'
                    'Файл autom_log находится в той же директории, что и программа.')
    lbl_fin.grid(column=3, row=10, padx=20, pady=20, sticky='s')
