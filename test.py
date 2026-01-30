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



a = 10
print(a)