import glob
import os
import shutil
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constants import ORIGINAL_TRACKS_FILE_PATH, SQLITE_QUERY_PATH, PROCESSING_TRACKS_FILE_PATH, DONE_FOLDER_NAME, \
    THREADS_NUMBER
from loggers import AppLogger


class PlaylistProcessor:
    def __init__(self, db_path):
        self.logger = AppLogger().get_logger()
        self.db_path = db_path
        self.total_tracks = 0
        self.tracks_in_success = []
        self.done_folder_path = Path(PROCESSING_TRACKS_FILE_PATH) / DONE_FOLDER_NAME
        if not os.path.exists(self.done_folder_path):
            os.makedirs(self.done_folder_path)

    def run(self):
        tracks = self.fetch_playlist_tracks()
        self.total_tracks = len(tracks)
        if tracks:
            with ThreadPoolExecutor(max_workers=THREADS_NUMBER) as executor:
                executor.map(self._move_tracks, [track for track in tracks])
            self._move_tracks(tracks)
        else:
            self.logger.warning('No tracks found in playlist!')

    def fetch_playlist_tracks(self):
        try:
            with open(SQLITE_QUERY_PATH, 'r') as file:
                query = file.read()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
            return results
        except Exception as e:
            self.logger.error(f'An error occurred while fetching playlist tracks: {e}')
            return None

    def _move_tracks(self, track):
        file_path, artist, title = track
        search_pattern = f"{ORIGINAL_TRACKS_FILE_PATH}/**/{file_path}"
        matching_files = glob.glob(search_pattern, recursive=True)
        if matching_files:
            source_path = matching_files[0]
            destination_path = self.done_folder_path / file_path
            try:
                if not destination_path.exists():
                    shutil.move(source_path, destination_path)
                    self.logger.info(f'Moved: {file_path}')
                    self.tracks_in_success.append((file_path, artist, title, destination_path))
                else:
                    self.logger.warning(f'Destination file already exists: {destination_path}')
            except Exception as e:
                self.logger.error(f'An error occurred while moving the file: {e}')
