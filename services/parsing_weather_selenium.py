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
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".js-input"))
        )
        city_name = city_name
        search_input.send_keys(city_name)
        sleep(1)

        dropdown_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.city-link"))
        )

        # находим нужный город и кликаем
        for item in dropdown_items:
            name_span = item.find_element(By.CSS_SELECTOR, "span.name")
            if city_name.lower() in name_span.text.lower():
                item.click()
                break
            else:
                error = "Такого города нет!"
                return error
        # sleep(2)

        # WebDriverWait(driver, 10).until(
        #     lambda d: d.execute_script(
        #         "return window.M && window.M.state && window.M.state.city && window.M.state.weather;"
        #     )
        # )

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
                "description": f"Температура воздуха: {data['weather']['cw']['temperatureAir'][0]}°C"
            },
            "feels_like": {
                "description": f"Ощущается как: {data['weather']['cw']['temperatureFeelsLike'][0]}°C"
            },
            "description": {
                "description": f"{data['weather']['cw']['description'][0]}"
            },
            "wind_speed": {
                "description": f"Скорость ветра до: {data['weather']['cw']['windSpeed'][0]}м/с"
            },
            "wind_gust": {
                "description": f"Порывы ветра до: {data['weather']['cw']['windGust'][0]}м/с"
            },
            "wind_direction": {
                "description": f"Направление ветра: {data['weather']['cw']['windDirection'][0]}°"
            },
            "humidity": {
                "description": f"Относительная влажность: {data['weather']['cw']['humidity'][0]}%"
            },
            "pressure": {
                "description": f"Давление: {data['weather']['cw']['pressure'][0]}мм рт. ст."
            },
            "precipitation": {
                "description": f"Осадки: {data['weather']['cw']['precipitation'][0]}мм"
            }
        }
    city = f"{data['city']['translations']['ru']['city']['name']}"
    icon_code = data['weather']['cw']['iconWeather'][0]
    icon = f"icons/{icon_code}.svg"
    b_n = data['weather']['cw']['colorBackground'][0].replace('-', '_')
    background_image = f"https://st.gismeteo.st/assets/bg-desktop-now/{b_n}.webp"
    temp = f"{data['weather']['cw']['temperatureAir'][0]}°C"
    return weather_info, city, icon, background_image, temp


