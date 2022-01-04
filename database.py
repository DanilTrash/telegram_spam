import pandas as pd


class Data:

    def __init__(self, sheet_name):
        self.file_name = 'telegram.xlsx'
        self.sheet_name = sheet_name

    def __call__(self, arg):
        self.data_frame = pd.read_excel(self.file_name, sheet_name=self.sheet_name, dtype={arg: str})
        values = self.data_frame[arg]
        return values
