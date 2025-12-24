import requests
from datetime import datetime


class ParsingCurrency:

    def __init__(self):
        self.currency_json = None
        self.year = None
        self.month = None
        self.day = None
        self.date = None
        self.get_datetime()

    def get_datetime(self):
        dt = datetime.now()
        self.year, self.month, self.day = dt.year, dt.month, dt.day

    def get_all_currency_json(self, y=None, m=None, d=None):
        y, m, d = y or self.year, m or self.month, d or self.day
        url = "https://api.nbrb.by/exrates/rates?ondate={}-{}-{}&periodicity=0".format(y, m, d)  # URL сайта (str)
        self.currency_json = requests.get(url=url).json()
        self.date = datetime(int(y), int(m), int(d)).strftime("%d.%m.%Y")
        return self.currency_json
