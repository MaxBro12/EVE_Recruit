from os.path import exists

from settings import (
    csv_file,
    csv_data,
)
from mybase import (
    create_csv,
)


def main_cheack():
    if not exists(csv_file):
        create_csv(csv_file, csv_data)
