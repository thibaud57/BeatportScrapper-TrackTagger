import json

import requests
from bs4 import BeautifulSoup
from constants import MAX_RETRIES, SCRIPT_ID, USER_AGENT
from enums import StatusCode


class RequestsHelper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': USER_AGENT}

    def search_track(self, search_url):
        for _ in range(MAX_RETRIES):
            try:
                response = self.session.get(search_url, headers=self.headers)
                print(f'With search url: {search_url} with status: {response.status_code}')

                if response.status_code == StatusCode.SUCCESS.value:
                    return self.crawler(response.content)

                elif response.status_code == StatusCode.FORBIDDEN.value:
                    print('Received a 403 status code. Retrying...')
                    continue

                else:
                    print(f'Failed to fetch the page. Status code: {response.status_code}')
                    return None

            except requests.RequestException as e:
                print(f"Request error: {e}")
                continue

        print('Max retries reached. Exiting.')
        return None

    @staticmethod
    def crawler(content):
        try:
            soup = BeautifulSoup(content, 'html.parser')
            script = soup.find('script', {'id': SCRIPT_ID})

            if not script:
                print(f"Script with ID {SCRIPT_ID} not found")
                return None

            return json.loads(script.string)
        except Exception as e:
            print(f"Error while parsing content: {e}")
            return None

    def close(self):
        self.session.close()
