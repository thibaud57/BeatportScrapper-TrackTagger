import json
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from constants import MAX_RETRIES, SCRIPT_ID, BEATPORT_SEARCH_URL, USER_AGENT, CHROME_DRIVER
from enums import StatusCode
from utils.utils import clean_string


class SeleniumHelper:
    def __init__(self):
        service = Service(executable_path=CHROME_DRIVER)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)

    def close(self):
        self.driver.quit()

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
                self.driver.get(search_url)

                try:
                    xpath_cookies_button = "//button[text()='Allow all cookies']"
                    WebDriverWait(self.driver, 1).until(
                        ec.element_to_be_clickable((By.XPATH, xpath_cookies_button))).click()
                except:
                    pass

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                script = soup.find('script', {'id': SCRIPT_ID})
                data = json.loads(script.string)
                return data

            elif response.status_code == StatusCode.FORBIDDEN.value:
                print('Received a 403 status code. Retrying...')
                continue

            else:
                print(f'Failed to fetch the page. Status code: {response.status_code}')
                return None

        print('Max retries reached. Exiting.')
        return None
