import glob
import json
import os
import shutil
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constants import ORIGINAL_TRACKS_FILE_PATH, PROCESSING_TRACKS_FILE_PATH, DONE_FOLDER_NAME, \
    THREADS_NUMBER
from enums import PlaylistType
from loggers import AppLogger


class PlaylistProcessor:
    def __init__(self, playlist_type, playlist_path):
        self.logger = AppLogger().get_logger()
        self.playlist_path = playlist_path
        self.playlist_type = playlist_type
        self.total_tracks = 0
        self.tracks_in_success = []
        self.tracks_in_failure = []
        self.done_folder_path = Path(PROCESSING_TRACKS_FILE_PATH) / DONE_FOLDER_NAME
        if not os.path.exists(self.done_folder_path):
            os.makedirs(self.done_folder_path)

    def run(self):
        tracks = self.fetch_playlist_tracks()
        self.total_tracks = len(tracks)
        if tracks:
            with ThreadPoolExecutor(max_workers=THREADS_NUMBER) as executor:
                executor.map(self._move_tracks, [track for track in tracks])
            # self._move_tracks(tracks)
        else:
            self.logger.warning('No tracks found in playlist!')

    def fetch_playlist_tracks(self):
        if self.playlist_type == PlaylistType.SQLITE.value:
            try:
                with open(self.playlist_path, 'r') as file:
                    query = file.read()
                with sqlite3.connect(self.playlist_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    results = cursor.fetchall()
                return results
            except Exception as e:
                self.logger.error(f'An error occurred while fetching playlist tracks from SQLite: {e}')
        elif self.playlist_type == PlaylistType.JSON.value:
            try:
                with open(self.playlist_path, 'r', encoding='utf-8') as file:
                    playlist = json.load(file)
                filtered_playlist = []
                for track in playlist:
                    if all(key in track for key in ['file_path', 'artist', 'title']):
                        filtered_playlist.append((track['file_path'], track['artist'], track['title']))
                return filtered_playlist
            except Exception as e:
                self.logger.error(f'An error occurred while fetching playlist tracks from JSON: {e}')
        else:
            self.logger.error(f'Unknown source type: {self.playlist_type}')
        return None

    def _move_tracks(self, track):
        file_path, artist, title = track
        path = Path(file_path).name
        # Glob have problem when [ ] are included in text pattern
        safe_path_for_glob = path.replace('[', '[[]')
        search_pattern = f"{ORIGINAL_TRACKS_FILE_PATH}/**/{safe_path_for_glob}"
        matching_files = glob.glob(search_pattern, recursive=True)
        if matching_files:
            source_path = matching_files[0]
            destination_path = self.done_folder_path / path
            try:
                if not destination_path.exists():
                    shutil.move(source_path, destination_path)
                    self.logger.info(f'Moved: {path}')
                    self.tracks_in_success.append((path, artist, title, destination_path))
                else:
                    self.logger.warning(f'Destination file already exists: {destination_path}')
            except Exception as e:
                self.logger.error(f'An error occurred while moving the file: {e}')
        else:
            self.logger.info(f'Failed: {path}')
            self.tracks_in_failure.append((path, artist, title))
