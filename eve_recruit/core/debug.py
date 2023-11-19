import logging
from typing import Union, Literal
from os import get_terminal_size


Level = Literal['debug', 'warning', 'info', 'error', 'crit']


def error_found(err):
    print(f"{'=' * (get_terminal_size()[0] - 1)}\nError logged:\n{err}")
    create_log_file(err)


def log_decorator(func):
    def wrapper(*args, **kwarks):
        func(*args, **kwarks)
        create_log_file(f'Function {func.__name__} called!')
    return wrapper


def create_log_file(
        log: Union[Exception, str],
        levelname: Level = 'debug',
        log_file: str = 'logger.log'
):
    """Добавляем в log_file данные log с указанием типа уровня:
    - debug - дебаг
    - warning - предупреждение
    - info - информация
    - error - ошибка
    - crit - критическая ошибка"""
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file,
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log_exc = False
    if type(log) != str:
        log_exc = True
    match levelname:
        case 'debug':
            logging.debug(log, exc_info=log_exc)
        case 'warning':
            logging.warning(log, exc_info=log_exc)
        case 'info':
            logging.info(log, exc_info=log_exc)
        case 'error':
            logging.error(log, exc_info=log_exc)
        case 'crit':
            logging.critical(log, exc_info=log_exc)
