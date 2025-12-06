from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from class_parsing_currencies import ParsingCurrencies
from class_parsing_films import ParsingPosterFilms

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        currency = ParsingCurrencies()
        films = ParsingPosterFilms()
        table = str(currency.table)
        films_row = films.get_films()
        return render_template('index.html', table=table, films=films_row)
    if request.method == "POST":
        pass
    return ""


# декоратор
@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == "GET":
        return render_template('about.html')
    if request.method == "POST":
        pass
    return ""


if __name__ == '__main__':
    app.run(debug=True)  # debug=True только в разработке
