import re

from os.path import exists, join, splitext

from debug import create_log_file
from start import main_cheack, create_prof
from mybase import Table
from settings import csv_file, profile_dir, accept
from clipb import write_to_cb, get_from_cp


def file_dir_creator(name: str = 'data') -> str:
    if len(splitext(name)) == 1:
        name += '.csv'
    name = join(profile_dir, name)
    return name


def load_profile() -> Table:
    profile = input('Введите название профиля:\n')
    if profile == '':
        profile = file_dir_creator()
        return Table(profile)
    else:
        profile_file = file_dir_creator(profile)
        if not exists(profile_file):
            ans = input(
                f'Профиль {profile} не существует!'
                'Создать? - Y / Повторить ввод - n'
            )
            if ans in accept:
                create_prof(profile_file)
                return Table(profile_file)
            else:
                return load_profile()


def main():
    # ! Проверка папки профиля
    main_cheack()

    # ! Подгрузка профиля
    base = load_profile()
    copy_msg = ''

    while True:
        ans = input('Скопируйте содержимое чата и нажмите enter\n')
        match ans:
            case '':
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

            case 'EXET':
                break

            case 'MERGE':
                ans = input('Через пробел введите названия профилей:\n')
                ans = ans.split(' ')


if __name__ == '__main__':
    try:
        main()
    except Exception as er:
        create_log_file(er)
        print(
            'Что-то пошло не так : (\n' +
            'Отправьте файл "error.log" разработчику!\n' +
            'maxbro126@gmail.com'
        )
