import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote_plus

from constants import TRACKS_FILE_PATH, MATCHING_SCORE_LIMIT, VALIDATE_KEY, BEATPORT_SEARCH_URL, THREADS_NUMBER
from enums import MusicFormat
from managers import MetadataManager, TrackManager
from scrappers import SeleniumHelper, TrackMatcher, BrowserPool
from utils import get_user_input


class TrackProcessor:
    def __init__(self):
        self.browser_pool = BrowserPool(size=THREADS_NUMBER)
        self.track_matcher = TrackMatcher()
        self.metadata_manager = MetadataManager()
        self.tracks_in_success = []
        self.tracks_file_path = Path(TRACKS_FILE_PATH)

    def run(self):
        urls_datas = self.build_search_urls()
        with ThreadPoolExecutor(max_workers=THREADS_NUMBER) as executor:
            executor.map(self.process_file, urls_datas)
        self.browser_pool.close_all()

    def build_search_urls(self):
        urls = []
        files = [f for f in os.listdir(self.tracks_file_path) if
                 os.path.isfile(os.path.join(self.tracks_file_path, f)) and f.endswith(MusicFormat.MP3.value)]
        for file in files:
            file_path = self.tracks_file_path / str(file)
            artist, title = self.metadata_manager.extract_metadata(file_path)
            search_url = f"{BEATPORT_SEARCH_URL + quote_plus(artist + ' ' + title)}"
            urls.append((search_url, file_path, artist, title))
        return urls

    def process_file(self, data):
        url, file_path, artist, title = data
        helper = SeleniumHelper(browser=self.browser_pool.get_browser())

        try:
            data = helper.search_track(url)
            if track_info_list := self.track_matcher.parse_track_info(data):
                best_match, best_score = self.track_matcher.find_best_match(artist.lower(), title.lower(), track_info_list)

                if best_match is None:
                    print('No best match found')
                else:
                    if best_score >= MATCHING_SCORE_LIMIT or get_user_input(best_match, best_score, artist, title) == VALIDATE_KEY:
                        manager = TrackManager(file_path, self.metadata_manager)
                        new_file_path = manager.run_track_processing_workflow(best_match)
                        if new_file_path:
                            self.tracks_in_success.append((file_path, artist, title, new_file_path))
        finally:
            self.browser_pool.return_browser(helper.driver)
