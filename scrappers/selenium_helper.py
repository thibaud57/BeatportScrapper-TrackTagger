import json
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from constants import MAX_RETRIES, SCRIPT_ID, BEATPORT_SEARCH_URL, USER_AGENT, CHROME_DRIVER
from enums import StatusCode
from utils.utils import clean_string


class SeleniumHelper:
    def __init__(self):
        service = Service(executable_path=CHROME_DRIVER)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)

    def search_track(self, artist, title):
        artist = clean_string(artist)
        title = clean_string(title)

        print(f'\nSearching track: {artist} - {title}')
        search_url = f"{BEATPORT_SEARCH_URL + quote_plus(artist + ' ' + title)}"
        headers = {'User-Agent': USER_AGENT}

        for _ in range(MAX_RETRIES):
            response = requests.get(search_url, headers=headers)
            print(f'With search url: {search_url} with status: {response.status_code}')

            if response.status_code == StatusCode.SUCCESS.value:
                return self.crawler(search_url)

            elif response.status_code == StatusCode.FORBIDDEN.value:
                print('Received a 403 status code. Retrying...')
                continue

            else:
                print(f'Failed to fetch the page. Status code: {response.status_code}')
                return None

        print('Max retries reached. Exiting.')
        return None

    def crawler(self, search_url):
        self.driver.get(search_url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        script = soup.find('script', {'id': SCRIPT_ID})
        data = json.loads(script.string)
        return data

    def close(self):
        self.driver.quit()
