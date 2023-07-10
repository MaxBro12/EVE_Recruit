from .debug import create_log_file
from .clipb import get_from_cp, write_to_cb
from .mybase import Table
from .filemanage import load_file, wayfinder


def clone_list(name_csv: str) -> bool:
    if not wayfinder(name_csv):
        create_log_file(f'Cant find csv file {name_csv}')
        return False

    copy_list = ''
    table = Table(name_csv)
    pilots = get_from_cp()
    pilots = pilots.split('\n')

    if len(pilots) > 0:
        for pilot in pilots:
            if table.add(pilot):
                if copy_list != '':
                    copy_list += ', ' + pilot
                else:
                    copy_list = pilot
        write_to_cb(copy_list)
        return True
    return False


def clone_theme(name_txt: str) -> bool:
    if not wayfinder(name_txt):
        create_log_file(f'Cant find txt file {name_txt}')
        return False
    write_to_cb(name_txt.split('.')[0])
    return True


def clone_letter(name_txt: str) -> bool:
    if not wayfinder(name_txt):
        create_log_file(f'Cant find txt file {name_txt}')
        return False
    write_to_cb(load_file(name_txt))
    return True
