import pandas as pd

from settings import csv_file


class Table():
    def __init__(self, name: str = None):
        self.table_name = ''
        if name is None:
            self.table_name = csv_file
        else:
            self.table_name = name

        self.data = self.load_csv()
        self.data.drop_duplicates()

    def load_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.table_name)

    def save_csv(self):
        self.data.to_csv(self.table_name, index=False)

    def add(self, pilot: str):
        if not self.find(pilot):
            self.data.loc[len(self.data)] = pilot
            self.save_csv()
            return True
        return False

    def find(self, pilot: str):
        return True if self.data['pilot'].isin([pilot]).any() else False


def create_csv(name: str, inner_data: dict) -> bool:
    pd.DataFrame([], columns=['pilot']).to_csv(name, index=False)
