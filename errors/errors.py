class UserError(Exception):
    """Базовое исключение для всех ошибок пользователя"""
    def __init__(self, message="Ошибка пользователя"):
        self.message = message
        super().__init__(message)


class UserNotFound(UserError):
    def __init__(self):
        super().__init__("Такого пользователя не существует!")


class WrongPassword(UserError):
    def __init__(self):
        super().__init__("Неверный пароль!")


class EmptyFieldsError(UserError):
    def __init__(self):
        super().__init__("Введите логин и пароль!")


class UserAlreadyExists(UserError):
    def __init__(self):
        super().__init__("Пользователь с таким логином уже существует!")


class InvalidUsername(UserError):
    def __init__(self):
        super().__init__("Введите корректный логин!")


class InvalidPassword(UserError):
    def __init__(self):
        super().__init__("Введите корректный пароль!")


class EmptyDateFieldsError(UserError):
    def __init__(self):
        super().__init__("Заполните все поля даты!")


class InvalidDateFormatError(UserError):
    def __init__(self):
        super().__init__("Дата должна содержать только цифры!")


class DateOutOfRangeError(UserError):
    def __init__(self):
        super().__init__("Введите корректную дату от 01.07.2016 до сегодня!")


class InvalidDateError(UserError):
    def __init__(self):
        super().__init__("Некорректная дата!")  # <- твой новый класс