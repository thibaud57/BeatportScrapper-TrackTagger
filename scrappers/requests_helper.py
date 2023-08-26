import json

import requests
from bs4 import BeautifulSoup

from constants import MAX_RETRIES, SCRIPT_ID, USER_AGENT
from enums import StatusCode
from loggers import AppLogger


class RequestsHelper:
    def __init__(self):
        self.logger = AppLogger().get_logger()
        self.session = requests.Session()
        self.headers = {'User-Agent': USER_AGENT}

    def search_track(self, search_url):
        for _ in range(MAX_RETRIES):
            try:
                response = self.session.get(search_url, headers=self.headers)
                self.logger.info(f'Search url: {search_url} with status: {response.status_code}')

                if response.status_code == StatusCode.SUCCESS.value:
                    return self.crawler(response.content)

                elif response.status_code == StatusCode.FORBIDDEN.value:
                    self.logger.warning('Received a 403 status code. Retrying...')
                    continue

                else:
                    self.logger.warning(f'Failed to fetch the page. Status code: {response.status_code}')
                    return None

            except requests.RequestException as e:
                self.logger.error(f'Request error: {e}')
                continue

        self.logger.warning('Max retries reached. Exiting.')
        return None

    def crawler(self, content):
        try:
            soup = BeautifulSoup(content, 'html.parser')
            script = soup.find('script', {'id': SCRIPT_ID})
            if not script:
                self.logger.warning(f'Script with ID {SCRIPT_ID} not found')
                return None
            try:
                return json.loads(script.string)
            except json.JSONDecodeError:
                self.logger.error('Error while loading json.')
                return None
        except Exception as e:
            self.logger.error(f'Error while parsing content: {e}')
            return None

    def close(self):
        self.session.close()
