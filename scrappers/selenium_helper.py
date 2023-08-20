import json

import requests
from bs4 import BeautifulSoup

from constants import MAX_RETRIES, SCRIPT_ID, USER_AGENT
from enums import StatusCode


class SeleniumHelper:
    def __init__(self, browser):
        self.driver = browser

    def search_track(self, search_url):
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
        try:
            self.driver.get(search_url)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            script = soup.find('script', {'id': SCRIPT_ID})

            if not script:
                print(f"Script with ID {SCRIPT_ID} not found on {search_url}")
                return None

            return json.loads(script.string)
        except Exception as e:
            print(f"Error while crawling {search_url}: {e}")
            return None

    def close(self):
        self.driver.quit()
