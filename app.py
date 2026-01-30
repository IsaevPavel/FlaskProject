from flask import Flask, render_template, request, session, redirect
from db.database import close_db
from datetime import datetime
from services.class_parsing_currencies import ParsingCurrency
from services.specified_date_for_parsing_currencies import specified_date_for_parsing_currencies
from services.class_parsing_films import ParsingFilms
from services.parsing_weather_selenium import parsing_weather
# from services.alternative_class_parsing_films import ParsingFilms
from errors.errors import UserError, EmptyFieldsError
from services.user_manager import register_user, login_user
from db.init_db import init_db
import os

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "db", "database.db")
app.teardown_appcontext(close_db)

app.secret_key = 'secret_key_for_session'  # обязательно для session
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
        weather, city, icon, icon2, background_image, temp, error_city = parsing_weather()
        weather_data = {
            "weather": weather,
            "city": city,
            "icon": icon,
            "icon2": icon2,
            "background_image": background_image,
            "temp": temp,
            "error_city": error_city
        }

        session.update(weather_data)

    currency_data = session['currency_data']
    date = session['date']

    error_city = None
    weather_data = {
        "error_city": error_city

    }
    session.update(weather_data)

    weather, city, icon, icon2, background_image, temp, error_city = (
        session.get("weather"),
        session.get("city"),
        session.get("icon"),
        session.get("icon2"),
        session.get("background_image"),
        session.get("temp"),
        session.get("error_city")
    )

    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "weather":
            city_from_form = request.form.get("city")
            weather, city, icon, icon2, background_image, temp, error_city = parsing_weather(city_from_form)
            if error_city is None:
                weather_data = {
                    "weather": weather,
                    "city": city,
                    "icon": icon,
                    "icon2": icon2,
                    "background_image": background_image,
                    "temp": temp,
                    "error_city": error_city

                }

            else:
                weather_data = {
                    "error_city": error_city

                }

            session.update(weather_data)

            weather, city, icon, icon2, background_image, temp, error_city = (
                session.get("weather"),
                session.get("city"),
                session.get("icon"),
                session.get("icon2"),
                session.get("background_image"),
                session.get("temp"),
                session.get("error_city")
            )
        elif form_type == "currency":
            error_message = None
            year = request.form.get("YEAR")
            month = request.form.get("MONTH")
            day = request.form.get("DAY")

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
    # print(weather)
    return render_template(
        'index.html',
        USERNAME=session_user,
        FILMS=films_row,
        DATE=date,
        CURRENCY=currency_data,
        WEATHER=weather,
        CITY=city,
        FIRST_ICON=icon,
        LAST_ICON=icon2,
        BACKGROUND_IMAGE=background_image,
        TEMPERATURE=temp,
        ERROR=error_message,
        ERROR_CITY=error_city
    )


@app.route('/login', methods=['POST'])
def login():
    login_error = None
    session_user = session.get("username")

    username = request.form.get("username")
    password = request.form.get("password")

    error_city = None
    weather_data = {
        "error_city": error_city

    }
    session.update(weather_data)

    weather, city, icon, icon2, background_image, temp, error_city = (
        session.get("weather"),
        session.get("city"),
        session.get("icon"),
        session.get("icon2"),
        session.get("background_image"),
        session.get("temp"),
        session.get("error_city")
    )

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
        WEATHER=weather,
        CITY=city,
        CURRENCY=currency_data,
        LOGIN_ERROR=login_error,
        FIRST_ICON=icon,
        LAST_ICON=icon2,
        BACKGROUND_IMAGE=background_image,
        TEMPERATURE=temp,
        ERROR_CITY=error_city
    )


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    error_city = None
    weather_data = {
        "error_city": error_city

    }
    session.update(weather_data)

    weather, city, icon, icon2, background_image, temp, error_city = (
        session.get("weather"),
        session.get("city"),
        session.get("icon"),
        session.get("icon2"),
        session.get("background_image"),
        session.get("temp"),
        session.get("error_city")
    )

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
        WEATHER=weather,
        CITY=city,
        FIRST_ICON=icon,
        LAST_ICON=icon2,
        BACKGROUND_IMAGE=background_image,
        TEMPERATURE=temp,
        REGISTER_ERROR=register_error,
        ERROR_CITY=error_city
    )


@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template("main.html")


@app.route('/test', methods=['GET', 'POST'])
def test():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        weather = parsing_weather(city)
    return render_template('test.html', CITY=weather)



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
