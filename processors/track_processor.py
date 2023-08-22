import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote_plus

from constants import TRACKS_FILE_PATH, MATCHING_SCORE_LIMIT, VALIDATE_KEY, BEATPORT_SEARCH_URL, THREADS_NUMBER
from enums import MusicFormat
from loggers import AppLogger
from managers import MetadataManager, TrackManager
from scrappers import TrackMatcher, RequestsHelper
from utils import get_user_input, add_original_name_to_title_if_needed


class TrackProcessor:
    def __init__(self):
        self.logger = AppLogger().get_logger()
        self.helper = RequestsHelper()
        self.track_matcher = TrackMatcher()
        self.metadata_manager = MetadataManager()
        self.tracks_file_path = Path(TRACKS_FILE_PATH)
        self.tracks_in_success = []
        self.tracks_to_confirm = []
        self.tracks_in_failure = []

    def run(self):
        urls_datas = self._build_search_urls()
        with ThreadPoolExecutor(max_workers=THREADS_NUMBER) as executor:
            executor.map(self._process_file, urls_datas)
        self._show_failure()
        self._confirm_and_process_tracks()

    def _build_search_urls(self):
        urls = []
        files = [f for f in os.listdir(self.tracks_file_path) if
                 os.path.isfile(os.path.join(self.tracks_file_path, f)) and f.endswith(MusicFormat.MP3.value)]
        for file in files:
            file_path = self.tracks_file_path / str(file)
            artist, title = self.metadata_manager.extract_metadata(file_path)
            search_url = f"{BEATPORT_SEARCH_URL + quote_plus(artist + ' ' + title)}"
            urls.append((search_url, file_path, artist, add_original_name_to_title_if_needed(title)))
        return urls

    def _process_file(self, data):
        url, file_path, artist, title = data
        data = self.helper.search_track(url)

        if track_info_list := self.track_matcher.parse_track_info(data):
            best_match, best_score = self.track_matcher.find_best_match(artist.lower(), title.lower(), track_info_list)

            if best_match is None:
                self.tracks_in_failure.append((artist, title))
            elif best_score <= MATCHING_SCORE_LIMIT:
                self.tracks_to_confirm.append((best_match, best_score, file_path, artist, title))
            else:
                self._process_track(best_match, file_path, artist, title)

    def _process_track(self, best_match, file_path, artist, title):
        manager = TrackManager(file_path, self.metadata_manager)
        new_file_path = manager.run_track_processing_workflow(best_match)
        if new_file_path:
            self.tracks_in_success.append((file_path, artist, title, new_file_path))

    def _show_failure(self):
        for artist, title in self.tracks_in_failure:
            self.logger.warning(f'Tracks in failure: \nNo best match found for: {artist} - {title}')

    def _confirm_and_process_tracks(self):
        for best_match, best_score, file_path, artist, title in self.tracks_to_confirm:
            self.logger.info('Tracks to confirm:')
            if get_user_input(best_match, artist, title) == VALIDATE_KEY:
                self._process_track(best_match, file_path, artist, title)
