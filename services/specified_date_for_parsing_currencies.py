from datetime import datetime
from errors.errors import EmptyDateFieldsError, InvalidDateFormatError, DateOutOfRangeError, InvalidDateError


def specified_date_for_parsing_currencies(year, month, day):
    if not year or not month or not day:
        raise EmptyDateFieldsError()

    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        raise InvalidDateFormatError()

    try:
        input_date = datetime(int(year), int(month), int(day))
    except ValueError:
        raise InvalidDateError()

    min_date = datetime(2016, 7, 1)
    max_date = datetime.today()

    if not (min_date <= input_date <= max_date):
        raise DateOutOfRangeError

    return input_date
