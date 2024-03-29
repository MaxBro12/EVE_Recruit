from pandas import (
    DataFrame,
    concat,
    read_csv,
    read_xml,
    read_json,
    read_sql,
    read_html,
    read_clipboard,
)
from io import StringIO

from os.path import splitext


class Table:
    """Класс для работы с csv файлами"""
    def __init__(
            self,
            file_name: str = '',
            sep: str = ',',
            index: bool = False,
    ):
        self.file_name = file_name
        self.sep = sep
        self.index = index
        self.data = DataFrame()
        self.data = read_csv(file_name, sep=sep)

    def save(self, type: str = 'csv'):
        self.data.to_csv(self.file_name, index=self.index)

    def add(self, pilot: str):
        if not self.find(pilot):
            self.data.loc[len(self.data)] = pilot
            self.save()
            return True
        return False

    def find(self, pilot: str):
        return True if self.data['pilot'].isin([pilot]).any() else False

    def merge(self, other):
        self.data = concat([self.data, other.data])
        self.save()


def create_csv(name: str, inner_data: dict = {}):
    DataFrame([], columns=['pilot']).to_csv(name, index=False)



if __name__ == "__main__":
    table = Table('')
