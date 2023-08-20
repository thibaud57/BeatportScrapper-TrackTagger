import os
from pathlib import Path

from constants import TRACKS_FILE_PATH, MATCHING_SCORE_LIMIT, VALIDATE
from enums import MusicFormat
from managers import MetadataManager, TrackManager
from scrappers import SeleniumHelper, TrackMatcher
from utils import get_user_input


class TrackProcessor:
    def __init__(self):
        self.helper = SeleniumHelper()
        self.track_matcher = TrackMatcher()
        self.metadata_manager = MetadataManager()
        self.tracks_in_success = []
        self.tracks_file_path = Path(TRACKS_FILE_PATH)

    def process_file(self, file):
        file_path = self.tracks_file_path / str(file)
        artist, title = self.metadata_manager.extract_metadata(file_path)

        data = self.helper.search_track(artist, title)

        if track_info_list := self.track_matcher.parse_track_info(data):
            best_match, best_score = self.track_matcher.find_best_match(artist, title, track_info_list)
            if best_match is None:
                print('No best match found')
            else:
                if best_score >= MATCHING_SCORE_LIMIT or get_user_input() == VALIDATE:
                    manager = TrackManager(file_path, self.metadata_manager)
                    new_file_path = manager.run_track_processing_workflow(best_match)
                    if new_file_path:
                        self.tracks_in_success.append((file_path, artist, title, new_file_path))

    def run(self):
        files = [f for f in os.listdir(self.tracks_file_path) if
                 os.path.isfile(os.path.join(self.tracks_file_path, f)) and f.endswith(MusicFormat.MP3.value)]
        for file in files:
            self.process_file(file)
