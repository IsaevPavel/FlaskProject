from flask import Flask, render_template, request, session, redirect
from datetime import datetime
from class_parsing_currencies import ParsingCurrency
from class_parsing_films import ParsingPosterFilms

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'  # обязательно для session


@app.route('/', methods=['GET', 'POST'])
def index():
    films = ParsingPosterFilms()
    films_row = films.get_films()
    error_message = None

    if 'currency_data' not in session:
        currency = ParsingCurrency()
        session['currency_data'] = currency.get_all_currency_json()
        session['date'] = currency.date

    currency_data = session['currency_data']
    date = session['date']

    # ===== POST =====
    if request.method == "POST":
        year = request.form.get("YEAR")
        month = request.form.get("MONTH")
        day = request.form.get("DAY")
        if not year or not month or not day:
            error_message = "Заполните все поля даты!"
        elif not (year.isdigit() and month.isdigit() and day.isdigit()):
            error_message = "Дата должна содержать только цифры!"
        else:
            try:
                input_date = datetime(int(year), int(month), int(day))
                min_date = datetime(2016, 7, 1)
                max_date = datetime.today()

                if not (min_date <= input_date <= max_date):
                    raise ValueError

                currency = ParsingCurrency()
                session['currency_data'] = currency.get_all_currency_json(y=year, m=month, d=day)
                session['date'] = input_date.strftime('%d.%m.%Y')

                currency_data = session['currency_data']
                date = session['date']

            except ValueError:
                error_message = "Введите корректную дату в формате DD-MM-YYYY!"
    return render_template(
        'index.html',
        FILMS=films_row,
        DATE=date,
        CURRENCY=currency_data,
        ERROR=error_message
    )


@app.route('/reset')
def reset_currency():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
