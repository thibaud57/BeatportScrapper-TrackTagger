import glob
import json
import os
import shutil
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import chardet

from constants import (ARTIST_TEXT_KEY, DONE_FOLDER_NAME, LOCATION_TEXT_KEY,
                       ORIGINAL_TRACKS_FILE_PATH, PROCESSING_TRACKS_FILE_PATH,
                       SQLITE_QUERY_PATH, THREADS_NUMBER, TRACK_TITLE_TEXT_KEY)
from enums import PlaylistKey, PlaylistType
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
        if tracks is not None:
            self.total_tracks = len(tracks)
            with ThreadPoolExecutor(max_workers=THREADS_NUMBER) as executor:
                executor.map(self._move_tracks, [track for track in tracks])
        else:
            self.logger.warning('No tracks found in playlist!')

    def fetch_playlist_tracks(self):
        match self.playlist_type:
            case PlaylistType.SQLITE.value:
                return self._extract_sqlite()
            case PlaylistType.JSON.value:
                return self._extract_json()
            case PlaylistType.TEXT.value:
                _json = self._convert_to_json()
                return self._extract_json(_json)
            case _:
                self.logger.error(f'Unknown source type: {self.playlist_type}')
        return None

    def _extract_sqlite(self):
        try:
            with open(SQLITE_QUERY_PATH, 'r') as file:
                query = file.read()
            with sqlite3.connect(self.playlist_path) as conn:
                def filename_collation(s1, s2):
                    return 1 if s1.lower() > s2.lower() else -1 if s1.lower() < s2.lower() else 0
                
                conn.create_collation("FILENAME", filename_collation)
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
            return results
        except Exception as e:
            self.logger.error(f'An error occurred while fetching playlist tracks from SQLite: {e}')

    def _extract_json(self, provided_json=None):
        try:
            if provided_json is not None:
                playlist = json.loads(provided_json)
            else:
                with open(self.playlist_path, 'r', encoding='utf-8') as file:
                    playlist = json.load(file)
            filtered_playlist = []
            for track in playlist:
                if all(key in track for key in
                       [PlaylistKey.FILE_PATH.value, PlaylistKey.ARTIST.value, PlaylistKey.TITLE.value]):
                    filtered_playlist.append((track[PlaylistKey.FILE_PATH.value], track[PlaylistKey.ARTIST.value],
                                              track[PlaylistKey.TITLE.value]))
            return filtered_playlist
        except Exception as e:
            self.logger.error(f'An error occurred while fetching playlist tracks from JSON: {e}')

    def _convert_to_json(self):
        try:
            with open(self.playlist_path, 'rb') as file:
                raw_data = file.read()
                encoding = chardet.detect(raw_data)['encoding']
            with open(self.playlist_path, 'r', encoding=encoding) as file:
                lines = file.readline()
                headers = lines.strip().split('\t')
                artist_index = headers.index(ARTIST_TEXT_KEY)
                title_index = headers.index(TRACK_TITLE_TEXT_KEY)
                file_path_index = headers.index(LOCATION_TEXT_KEY)
                data = []
                for line in file:
                    fields = line.strip().split('\t')
                    data.append({
                        PlaylistKey.ARTIST.value: fields[artist_index],
                        PlaylistKey.TITLE.value: fields[title_index],
                        PlaylistKey.FILE_PATH.value: fields[file_path_index]
                    })
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f'An error occurred while converting playlist text to JSON: {e}')

    def _move_tracks(self, track):
        # Handle different track formats based on the extraction method
        if isinstance(track, tuple) and len(track) == 1:
            # SQLite case - Only filename
            file_path = track[0]
            artist = "Osef"
            title = "Osef"
        elif isinstance(track, tuple) and len(track) == 3:
            # JSON/TEXT case - Full information
            file_path, artist, title = track
        else:
            self.logger.error(f'Unexpected track format: {track}')
            return
            
        path = Path(file_path).name
        # Glob have problem when [ ] are included in text pattern
        safe_path_for_glob = path.replace('[', '[[]')
        search_pattern = f"{Path(ORIGINAL_TRACKS_FILE_PATH)}/**/{safe_path_for_glob}"
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
            self.tracks_in_failure.append((artist, title))
