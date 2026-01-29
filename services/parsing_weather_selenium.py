from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep





def parsing_weather(city_name=None):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.gismeteo.by/weather-minsk-4248/")

    if city_name:
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".js-input"))
        )
        search_input.send_keys(city_name)

        dropdown_items = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.group.found"))
        )
        # находим нужный город и кликаем
        for item in dropdown_items:
            name_span = item.find_element(By.CSS_SELECTOR, "span.name")
            if city_name.lower() in name_span.text.lower():
                driver.execute_script("arguments[0].click();", name_span)
                break
        else:
            error = "Такого города нет!"
            return error

        # выполнить JS и получить объект
    data = driver.execute_script("""
    return {
        city: window.M.state.city,
        weather: window.M.state.weather
    };
    """)
    driver.quit()

    weather_info = {
            "temperature": {
                "description": "Температура воздуха",
                "value": f"{data['weather']['cw']['temperatureAir'][0]}°C"
            },
            "feels_like": {
                "description": "Ощущается как",
                "value": f"{data['weather']['cw']['temperatureFeelsLike'][0]}°C"
            },
            "description": {
                "description": f"{data['weather']['cw']['description'][0]}",
                "value": ""
            },
            "wind_speed": {
                "description": "Скорость ветра до",
                "value": f"{data['weather']['cw']['windSpeed'][0]}м/с"
            },
            "wind_gust": {
                "description": "Порывы ветра до",
                "value": f"{data['weather']['cw']['windGust'][0]}м/с"
            },
            "wind_direction": {
                "description": "Направление ветра",
                "value": f"{data['weather']['cw']['windDirection'][0]}°"
            },
            "humidity": {
                "description": "Относительная влажность",
                "value": f"{data['weather']['cw']['humidity'][0]}%"
            },
            "pressure": {
                "description": "Давление",
                "value": f"{data['weather']['cw']['pressure'][0]}мм"
            },
            "precipitation": {
                "description": "Осадки",
                "value": f"{data['weather']['cw']['precipitation'][0]}мм"
            }
        }
    city = f"{data['city']['translations']['ru']['city']['name']}"
    icon_code = data['weather']['cw']['iconWeather'][0]
    print(icon_code)
    icon = icon_code
    icon2 = None
    if icon_code.count("_") >= 2:
        find_code = icon_code.rfind("_")
        icon = icon_code[:find_code]
        icon2 = icon_code[find_code + 1:]
    b_n = data['weather']['cw']['colorBackground'][0].replace('-', '_')
    background_image = f"https://st.gismeteo.st/assets/bg-desktop-now/{b_n}.webp"
    temp = f"{data['weather']['cw']['temperatureAir'][0]}°C"
    print(icon, icon2)
    return weather_info, city, icon, icon2, background_image, temp

# print(parsing_weather("Несвиж"))

