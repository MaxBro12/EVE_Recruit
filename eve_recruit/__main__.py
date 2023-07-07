from core import (
    create_log_file,
)
from start import main_check


def main():
    profiles, conf = main_check()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        create_log_file(err)
        print(
            'Что-то пошло не так : (\n' +
            'Отправьте файл "error.log" разработчику!\n' +
            'maxbro126@gmail.com'
        )
