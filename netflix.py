import datetime as dt
from pprint import pprint

from lan import languages

from selenium import webdriver
import pickle
import time
import pyperclip
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import pandas
import json
from movie_categories import movie_categories


class Netflix:
    def __init__(self):
        self.all_urls = []
        self.dict_list = []
        self.flag_cookie = True
        self.chrome_driver_path = "C:\Development\chromedriver.exe"
        self.url_base = "https://netflix.com/hu/"
        self.EMAIL = 'xxx'
        self.PASSWORD = 'xxx'


    def make_urls(self):
        driver = webdriver.Chrome(self.chrome_driver_path)
        driver.get(f"{self.url_base}browse/genre/34399")

        to_login_button = driver.find_element_by_css_selector('a.authLinks')
        to_login_button.click()
        time.sleep(1)

        email_field = driver.find_element_by_id('id_userLoginId')
        password_field = driver.find_element_by_id('id_password')
        login_button = driver.find_element_by_css_selector('.login-button')

        pyperclip.copy("@")
        email_field.send_keys(self.EMAIL)
        password_field.send_keys(self.PASSWORD)
        login_button.click()
        time.sleep(2)

        profile = driver.find_element_by_css_selector('.profile-link')
        profile.click()

        grid_button = driver.find_element_by_css_selector('.aro-grid-toggle')
        grid_button.click()

        drop_down = driver.find_element_by_css_selector('.nfDropDown')
        drop_down.click()

        a_to_z = driver.find_elements_by_css_selector('.nfDropDown ul li')[2]
        a_to_z.click()

        not_on_bottom = True

        while not_on_bottom:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            height = driver.execute_script("return document.documentElement.scrollHeight")
            scroll = driver.execute_script("return document.documentElement.scrollTop")
            client_height = driver.execute_script("return document.documentElement.clientHeight")
            print(height, scroll + client_height)
            if scroll + client_height >= height - 1:
                not_on_bottom = False

        films = driver.find_elements_by_css_selector('.galleryLockups .slider-item .ptrack-content a')

        links = []

        for film in films:
            url = film.get_attribute('href')
            url = url.split('?')[0]
            links.append(url)

        print(len(links))

        with open(f'netflix-urls.json', 'w', encoding='utf-8') as f:
            json.dump(links, f, ensure_ascii=False, indent=4)

        driver.quit()

    def clean_string(self, string):
        string = string.strip()
        if string[-1] == ',':
            string = string[:-1]

        return string

    def translate(self, string):
        verbs = string.split(' ')

        translated = []
        for verb in verbs:
            lan_element = next((item for item in languages if item['en'] == verb), { 'en': 'not found', 'hun': 'not found' })
            if lan_element['en'] == 'not found':
                translated.append(verb)
            else:
                translated.append(lan_element['hun'])

        return ' '.join(translated)

    def get_data(self):
        driver = webdriver.Chrome(self.chrome_driver_path)

        # links = self.all_urls[180:183]

        for link in self.all_urls:
            driver.get(link)
            time.sleep(1)

            try:
                data = driver.find_element_by_xpath('/html/head/script[1]').get_attribute('innerHTML')

                data = json.loads(data)

                audio = []
                audios = driver.find_elements_by_css_selector('.more-details-item.item-audio')
                for audi in audios:
                    audio_text = self.clean_string(audi.text)
                    audio_text = audio_text.split(' - ')[0]
                    audio_text = self.translate(audio_text)
                    if audio_text not in audio:
                        audio.append(audio_text)

                subtitle = []
                subtitles = driver.find_elements_by_css_selector('.more-details-item.item-subtitle')
                for subt in subtitles:
                    subtitle_text = self.clean_string(subt.text)
                    subtitle.append(subtitle_text)
                genre = [data['genre']]
                genres = driver.find_elements_by_css_selector('a.more-details-item.item-genres')
                for gen in genres:
                    gen_text = gen.text.strip()
                    if gen_text not in genre:
                        genre.append(gen_text)
            except:
                pass
            else:
                data['dateCreated'] = data['dateCreated'].split('-')[0]
                data['trailer'] = []
                data['audio'] = ', '.join(audio)
                data['subtitleLanguage'] = ', '.join(subtitle)
                data['genre'] = genre
                data['provider'] = 'Netflix'
                data['url'] = link
                data['image'] = [
                    {
                        "@type": "ImageObject",
                        "url": data['image']
                    }
                ]
                data['actor'] = data.pop('actors')

                self.dict_list.append(data)

        data = {
            "date": dt.datetime.now().strftime('%Y. %m. %d.'),
            "movies": self.dict_list
        }

        with open(f'netflix-movies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        driver.quit()

    def read_urls_from_json(self):
        with open('netflix-urls.json') as netflix_links:
            self.all_urls = json.load(netflix_links)

