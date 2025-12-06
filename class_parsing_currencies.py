import requests
from bs4 import BeautifulSoup


class ParsingCurrencies:
    url_table = "https://www.nbrb.by/"

    def __init__(self):
        self.table = None
        self.get_table()

    def get_table(self):
        response = requests.get(self.url_table)
        soup = BeautifulSoup(response.text, "html.parser")
        table_currency = soup.find(id="p4")
        self.table = table_currency.find("table")
