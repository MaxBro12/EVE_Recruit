from sys import argv

from debug import create_log_file
from start import main_cheack
from mybase import Table
from settings import csv_file
from clipb import write_to_cb


def main(args: list):
    main_cheack()
    base = Table(csv_file)
    copy_msg = ''

    while True:
        pilot = input(': ')
        if pilot == '':
            write_to_cb(copy_msg)
            print(copy_msg)
            print('Список пилотов для рассылки сохранен в буфер')
        else:
            if base.add(pilot):
                print('НОВЫЙ ПИЛОТ: ' + pilot)
                if copy_msg != '':
                    copy_msg += ', ' + pilot
                else:
                    copy_msg = pilot
            else:
                print('УЖЕ В БАЗЕ: ' + pilot)


if __name__ == '__main__':
    try:
        argv.pop(0)
        if argv == []:
            argv = None
        main(argv)
    except Exception as er:
        create_log_file(er)
        print(
            'Что-то пошло не так : (\n' +
            'Отправьте файл "error.log" разработчику!\n' +
            'maxbro126@gmail.com'
        )
