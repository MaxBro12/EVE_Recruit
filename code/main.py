from sys import argv
import os

from debug import create_log_file
from start import main_cheack
from mybase import Table
from settings import csv_file
from clipb import write_to_cb, get_from_cp


def main(args: list = None):
    main_cheack()
    base = Table(csv_file)
    copy_msg = ''

    while True:
        ans = input('Скопируйте содержимое чата и нажмите enter\n')
        if ans == '':
            pilots = get_from_cp()

            if ',' in pilots:
                continue

            pilots = pilots.split('\n')

            if len(pilots) > 0:
                for pilot in pilots:
                    if base.add(pilot):
                        if copy_msg != '':
                            copy_msg += ', ' + pilot
                        else:
                            copy_msg = pilot
                print('Список пилотов для рассылки сохранен в буфер:')
                write_to_cb(copy_msg)
                print(copy_msg)
                copy_msg = ''
        elif ans == 'EXET':
            break


if __name__ == '__main__':
    try:
        main(argv)
    except Exception as er:
        create_log_file(er)
        print(
            'Что-то пошло не так : (\n' +
            'Отправьте файл "error.log" разработчику!\n' +
            'maxbro126@gmail.com'
        )
