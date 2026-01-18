from errors.errors import UserNotFound, WrongPassword, EmptyFieldsError
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import get_db


def find_user(username):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()


def create_user(username, password_hash):
    db = get_db()
    db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    db.commit()


def register_user(username, password):
    password_hash = generate_password_hash(password)
    user = find_user(username)

    if user is None:
        create_user(username, password_hash)
        message = f"Пользователь {username} успешно создан!"
    else:
        message = "Такой пользователь уже существует!"

    return message


def login_user(username, password):
    if not username or not password:
        raise EmptyFieldsError()
    else:
        user = find_user(username)

        if user is None:
            raise UserNotFound()

        if not check_password_hash(user["password_hash"], password):
            raise WrongPassword()

        return username