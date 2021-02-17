from selenium import webdriver
import time
import json
from movie_categories import movie_categories
import datetime as dt


class HBO:
    def __init__(self):
        self.all_urls = []
        self.dict_list = []
        self.flag_cookie = True
        self.chrome_driver_path = "C:\Development\chromedriver.exe"
        self.url_base = "https://hbogo.hu/filmek/"

    def make_url_list(self):
        driver = webdriver.Chrome(self.chrome_driver_path)
        for movie_category in movie_categories:
            driver.get(f"{self.url_base}{movie_category['url-part']}")
            time.sleep(1)

            if self.flag_cookie:
                cookie_btn = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
                cookie_btn.click()
                self.flag_cookie = False

            movie_list = driver.find_elements_by_css_selector('.grid-item a.item-link')

            url_list = []

            for movie in movie_list:
                url = movie.get_attribute('href')
                url_list.append(url)

                if url not in self.all_urls:
                    self.all_urls.append(url)

        with open(f'hbo-urls.json', 'w', encoding='utf-8') as file:
            json.dump(self.all_urls, file, ensure_ascii=False, indent=4)

        driver.quit()

    def get_url_list(self):
        return self.all_urls

    def get_data(self):
        driver = webdriver.Chrome(self.chrome_driver_path)

        for url in self.all_urls:
            driver.get(url)
            time.sleep(1)

            try:
                data_tag = driver.find_element_by_css_selector('.modal .rich-snippet script')
            except:
                pass
            else:
                data_json = data_tag.get_attribute('innerHTML')
                data_dict = json.loads(data_json)
                data_dict['provider'] = 'HBO'
                self.dict_list.append(data_dict)

        data = {
            "date": dt.datetime.now().strftime('%Y. %m. %d'),
            "movies": self.dict_list
        }

        with open(f'hbo-movies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        driver.quit()

    def read_urls_from_json(self):
        with open('hbo-urls.json') as hbo_links:
            self.all_urls = json.load(hbo_links).movies
