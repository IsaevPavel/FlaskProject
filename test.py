# gunicorn app:app
import os

print("Chromium exists:", os.path.exists("/usr/bin/chromium"))
print("Chromedriver exists:", os.path.exists("/usr/bin/chromedriver"))
