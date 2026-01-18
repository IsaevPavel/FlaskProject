from flask import Flask, render_template, request, session, redirect
from db.database import close_db
from datetime import datetime
from services.class_parsing_currencies import ParsingCurrency
from services.specified_date_for_parsing_currencies import specified_date_for_parsing_currencies
from services.class_parsing_films import ParsingFilms
# from services.alternative_class_parsing_films import ParsingFilms
from errors.errors import UserError, EmptyFieldsError
from services.user_manager import register_user, login_user
from db.init_db import init_db
import os

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "db", "database.db")
app.teardown_appcontext(close_db)

app.secret_key = 'secret_key_for_session'  # обязательно для session
users = {}
films = ParsingFilms()
films_row = films.get_films()


@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    session_user = session.get("username")

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
        error_message = None

        try:
            specified_date_for_parsing_currencies(year, month, day)
        except UserError as error:
            error_message = error.message

        if error_message is None:
            currency = ParsingCurrency()
            session['currency_data'] = currency.get_all_currency_json(y=year, m=month, d=day)
            session['date'] = datetime(int(year), int(month), int(day)).strftime('%d.%m.%Y')

            currency_data = session['currency_data']
            date = session['date']

    return render_template(
        'index.html',
        USERNAME=session_user,
        FILMS=films_row,
        DATE=date,
        CURRENCY=currency_data,
        ERROR=error_message
    )


@app.route('/login', methods=['POST'])
def login():
    login_error = None
    session_user = session.get("username")

    username = request.form.get("username")
    password = request.form.get("password")

    try:
        if not username or not password:
            raise EmptyFieldsError()

        session["username"] = login_user(username, password)
        session_user = session["username"]
    except UserError as error:
        login_error = error.message

    date = session.get('date')
    currency_data = session.get('currency_data')

    return render_template(
        "index.html",
        USERNAME=session_user,
        FILMS=films_row,
        DATE=date,
        CURRENCY=currency_data,
        LOGIN_ERROR=login_error
    )


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        if not username or not password:
            raise EmptyFieldsError()

        register_error = register_user(username, password)
    except UserError as error:
        register_error = error.message
    date = session.get('date')
    currency_data = session.get('currency_data')
    session_user = session.get("username")
    return render_template(
        "index.html",
        USERNAME=session_user,
        FILMS=films_row,
        DATE=date,
        CURRENCY=currency_data,
        REGISTER_ERROR=register_error
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
    with app.app_context():
        init_db()

    app.run(debug=True)
