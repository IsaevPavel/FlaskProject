import requests
from bs4 import BeautifulSoup
import textwrap

class ParsingFilms:
    def __init__(self):
        self.url = "https://afisha.me/"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.list_li = []
        self.get_li()

    def get_li(self):
        elm_ul = self.soup.find_all("ul", class_="b-lists list_afisha col-5")
        for ul in elm_ul:
            for li in ul.find_all("li"):
                self.list_li.append(li)
        # for ul in uls:
        #     parent = ul.parent
        #     if parent and parent.get("id") == "events-block":
        #         for li in ul.find_all("li"):
        #             self.list_li.append(li)

    def get_title(self):
        result = ["Список фильмов:"]
        for li in self.list_li:
            title = li.find_all("a", class_="name")[0].get_text(strip=True)
            result.append(f"Название: {title}")
        return result

    def get_films(self):
        result = []
        # print(self.list_li)
        for li in self.list_li:
            result.append({"title": li.find("a", class_="name").get_text(strip=True),
                           "url": li.find("a", class_="name").get("href"),
                           "image": li.find("a", class_="media").find("img").get("src")})
        return result

    def get_image(self):
        result = ["\nСсылки на картинки:"]
        for li in self.list_li:
            picture = li.find_all("a", class_="media")[0]
            title = picture.find("img").get("alt").strip()
            img_src = picture.find("img").get("src")
            result.append(f"{title}\n{img_src}")
        return result

    def get_description(self):
        result = ["\nОписание фильмов:"]
        for li in self.list_li[:10]:
            response = requests.get(li.find_all("a", class_="name")[0].get("href"))
            soup = BeautifulSoup(response.text, "lxml")
            title = li.find_all("a", class_="name")[0].get_text(strip=True)
            description = soup.find_all(class_="b-article post")[0].get_text(strip=True)
            result.append(f"Название: {title}\nОписание: {textwrap.fill(description, width=205)}\n")
        return result

