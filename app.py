from flask import Flask, render_template, request, session, redirect, jsonify
from datetime import datetime
from class_parsing_currencies import ParsingCurrency
# from class_parsing_films import ParsingFilms
from alternative_class_parsing_films import ParsingFilms
import hashlib

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'  # обязательно для session
users = {}
films = ParsingFilms()
films_row = films.get_films()


@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    username = session.get("username")

    if 'currency_data' not in session:
        currency = ParsingCurrency()
        session['currency_data'] = currency.get_all_currency_json()
        session['date'] = currency.date

    currency_data = session['currency_data']
    date = session['date']

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
                error_message = "Введите корректную дату от 01.07.2016 до сегодня!"

    return render_template(
        'index.html',
        FILMS=films_row,
        DATE=date,
        CURRENCY=currency_data,
        ERROR=error_message,
        USERNAME=username
    )


@app.route('/login', methods=['POST'])
def login():
    login_error = None

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        login_error = "Заполните форму!"

    elif username in users:
        input_hash = hashlib.sha256(password.encode()).hexdigest()

        if users[username] == input_hash:
            session["username"] = username
        else:
            login_error = "Неверный пароль!"
    else:
        login_error = "Такого логина не существует!"

    date = session.get('date')
    currency_data = session.get('currency_data')

    if "username" in session:
        return render_template(
            "index.html",
            USERNAME=session["username"],
            FILMS=films_row,
            DATE=date,
            CURRENCY=currency_data,
            LOGIN_ERROR=login_error
        )
    return render_template(
        "index.html",
        FILMS=films_row,
        DATE=date,
        CURRENCY=currency_data,
        LOGIN_ERROR=login_error
    )


@app.route('/register', methods=['POST'])
def register():
    register_error = None
    username = request.form.get("username")
    password = request.form.get("password")

    if "username" in session:
        log_in = session["username"]
    else:
        log_in = None

    if not username or not password:
        register_error = "Заполните форму!"
    elif not username in users:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users[username] = password_hash
        register_error = f"{username} регистрация прошла успешно"
    else:
        register_error = "Такой логин уже существует"
    date = session.get('date')
    currency_data = session.get('currency_data')
    return render_template(
        "index.html",
        REGISTER_ERROR=register_error,
        FILMS=films_row,
        DATE=date,
        CURRENCY=currency_data,
        USERNAME=log_in
    )


@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template("main.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/reset')
def reset():
    session.pop('currency_data', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
