from queue import Queue

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from constants import CHROME_DRIVER


class BrowserPool:
    def __init__(self, size):
        self._pool = Queue(maxsize=size)
        for _ in range(size):
            service = Service(executable_path=CHROME_DRIVER)
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            # options.add_argument('--no-sandbox')
            # options.add_argument('--disable-dev-shm-usage')
            browser = webdriver.Chrome(service=service, options=options)
            self._pool.put(browser)

    def get_browser(self):
        return self._pool.get()

    def return_browser(self, browser):
        self._pool.put(browser)

    def close_all(self):
        while not self._pool.empty():
            browser = self._pool.get()
            browser.quit()
