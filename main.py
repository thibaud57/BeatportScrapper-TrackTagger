from pathlib import Path

from pandas import read_csv

from constants import CSV_FILE_PATH, TRACKS_FILE_PATH, VALIDATE, DELIMITER, MATCHING_SCORE_LIMIT
from enums import CsvField, TrackInfo
from loggers import SuccessLog
from managers import MetadataManager, TrackManager
from scrappers import SeleniumHelper, TrackMatcher
from utils import get_user_input

csv_file_path = Path(CSV_FILE_PATH)
tracks_file_path = Path(TRACKS_FILE_PATH)

with open(csv_file_path, 'r') as f:
    df = read_csv(csv_file_path, delimiter=DELIMITER, encoding='utf-8')
    helper = SeleniumHelper()
    track_matcher = TrackMatcher()
    metadata_manager = MetadataManager()
    try:
        tracks_in_success = []
        for index, row in df.iterrows():
            file_path = tracks_file_path / row[CsvField.FILENAME.value]
            artist, title = row[CsvField.NAME.value], row[CsvField.TITLE.value]
            data = helper.search_track(artist, title)
            if track_info_list := track_matcher.parse_track_info(data):
                best_match, best_score = track_matcher.find_best_match(row, track_info_list)
                if best_match is None:
                    print("No best match found")
                else:
                    print(f"Best match: {best_match[TrackInfo.ARTISTS.value]} - {best_match[TrackInfo.TITLE.value]}")
                    print(best_score)
                    if best_score >= MATCHING_SCORE_LIMIT or get_user_input() == VALIDATE:
                        manager = TrackManager(file_path, metadata_manager)
                        new_file_path = manager.run_track_processing_workflow(best_match)
                        if new_file_path:
                            tracks_in_success.append((row[CsvField.FILENAME.value], new_file_path))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        success_log = SuccessLog(tracks_in_success, tracks_file_path)
        success_log.write_success_log()
        helper.close()
