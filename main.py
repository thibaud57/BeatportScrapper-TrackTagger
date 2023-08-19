import os
from pathlib import Path

from constants import TRACKS_FILE_PATH, VALIDATE, MATCHING_SCORE_LIMIT
from enums import TrackInfo, MusicFormat
from loggers import SuccessLog
from managers import MetadataManager, TrackManager
from scrappers import SeleniumHelper, TrackMatcher
from utils import get_user_input

tracks_file_path = Path(TRACKS_FILE_PATH)
tracks_in_success = []

helper = SeleniumHelper()
track_matcher = TrackMatcher()
metadata_manager = MetadataManager()

try:
    print('###START###')
    files = [f for f in os.listdir(tracks_file_path) if os.path.isfile(os.path.join(tracks_file_path, f))]

    for file in files:
        if file.endswith(MusicFormat.MP3.value):
            file_path = tracks_file_path / str(file)
            artist, title = metadata_manager.extract_metadata(file_path)

            data = helper.search_track(artist, title)

            if track_info_list := track_matcher.parse_track_info(data):
                best_match, best_score = track_matcher.find_best_match(artist, title, track_info_list)
                if best_match is None:
                    print('No best match found')
                else:
                    if best_score >= MATCHING_SCORE_LIMIT or get_user_input() == VALIDATE:
                        manager = TrackManager(file_path, metadata_manager)
                        new_file_path = manager.run_track_processing_workflow(best_match)
                        if new_file_path:
                            tracks_in_success.append((file_path, artist, title, new_file_path))
except Exception as e:
    print(f'An error occurred: {e}')
finally:
    success_log = SuccessLog(tracks_in_success, tracks_file_path)
    success_log.write_success_log()
    helper.close()
    print('\n###END###')
