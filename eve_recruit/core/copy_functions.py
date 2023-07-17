from .debug import create_log_file
from .clipb import get_from_cp, write_to_cb
from .mybase import Table
from .filemanage import load_file, wayfinder

from re import fullmatch

from settings import pilot_pattern


def clone_list(name_csv: str) -> str:
    if not wayfinder(name_csv):
        create_log_file(f'Cant find csv file {name_csv}')
        return ''

    copy_list = ''
    table = Table(name_csv)
    pilots = get_from_cp()
    pilots = pilots.split('\n')

    if len(pilots) > 0:
        for pilot in pilots[:50]:
            if fullmatch(pilot_pattern, pilot):
                if table.add(pilot):
                    if copy_list != '':
                        copy_list += ', ' + pilot
                    else:
                        copy_list = pilot
        write_to_cb(copy_list)
        create_log_file(
            f'List of pilots copied: {len(pilots)}',
            levelname='info'
        )
        return copy_list
    create_log_file('No pilots in call', 'info')
    return ''


def clone_theme(name_txt: str) -> str:
    ans = name_txt.split('.')[0]
    write_to_cb(ans)
    create_log_file(f'Theme copied: {ans}', levelname='info')
    return ans


def clone_letter(name_txt: str) -> str:
    if not wayfinder(name_txt):
        create_log_file(f'Cant find txt file {name_txt}')
        return ''
    ans = load_file(name_txt)
    write_to_cb(ans)
    create_log_file(f'Letter copied', levelname='info')
    return ans
