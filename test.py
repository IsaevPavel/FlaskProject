# Считаем строки во всех нужных файлах, исключая .venv и __pycache__
# $types = "*.py","*.html","*.js","*.css"
#
# $totalLines = 0
# foreach ($type in $types) {
#     $lines = Get-ChildItem -Recurse -Include $type | Where-Object { $_.FullName -notmatch '\\\.venv\\|\\__pycache__\\' } | Get-Content | Measure-Object -Line
#     Write-Output "$type : $($lines.Lines) строк"
#     $totalLines += $lines.Lines
# }
# Write-Output "Всего строк: $totalLines"



from datetime import datetime, timedelta
from time import sleep

# Тема 1. Пример типа данных результата при возвращении через запятую

# Функция возвращает какая у вас ОС (а так же сепаратор)
def get_os():
    if __file__[0] == "/":
        return "/", "Unix"  # type(<class 'tuple'>) Кортеж
    else:
        return "\\", "Windows"  # type(<class 'tuple'>) Кортеж


print("Показать тип возвращаемых данных:", type(get_os()))

# Задать значение двум и более переменным можно через одно значение вида КОРТЕЖ
x, y = ("435", "23423")
print("Значение двух переменных:", x, y)


# Тема 2. Цикл по времени

def tm(value):
    return str(value).split(" ", maxsplit=1)[1]


print()
start_time = datetime.now()  # Время СТАРТА
end_time = start_time + timedelta(seconds=5)  # Время КОНЦА
print("Время старта: {} | Время конца: {}".format(tm(start_time), tm(end_time)))
count = 0
while end_time >= datetime.now():
    count += 1
    print("{}. Текст напечатан в {}".format(count, tm(datetime.now())))
    sleep(1)

# 30 (Время старта)
# 30 + 5 (Максимальное время)
# 35 > 31 (Делаем)
# 35 > 32 (Делаем)
# 35 > 33 (Делаем)
# 35 > 34 (Делаем)
# 35 > 35 (Остановка)
