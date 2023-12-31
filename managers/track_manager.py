import os
import shutil

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from constants import DONE_FOLDER_NAME
from enums import ID3Metadata, MusicFormat
from loggers import AppLogger
from utils import clean_filename


class TrackManager:
    def __init__(self, file_path, metadata_manager):
        self.logger = AppLogger().get_logger()
        self.file_path = file_path
        self.metadata_manager = metadata_manager

    def run_track_processing_workflow(self, track_matching):
        try:
            self.metadata_manager.delete_metadata(self.file_path)
            self.metadata_manager.update_metadata(self.file_path, track_matching)
            self._rename_track()
            return self._move_track_to_done_folder()  # Workflow completed successfully
        except FileNotFoundError:
            self.logger.error(f'File not found: {self.file_path}')
            return None  # An error occurred during the workflow
        except ID3NoHeaderError:
            self.logger.error(f"'{self.file_path}' doesn't start with an ID3 tag")
        return None  # An error occurred during the workflow

    def _rename_track(self):
        audio = EasyID3(self.file_path)
        artist = clean_filename(', '.join(audio.get(ID3Metadata.ARTIST.value, [])))
        title = clean_filename(', '.join(audio.get(ID3Metadata.TITLE.value, [])))
        new_filename = f'{artist} - {title}{MusicFormat.MP3.value}'
        new_file_path = os.path.join(os.path.dirname(self.file_path), new_filename)
        os.rename(self.file_path, new_file_path)
        self.file_path = new_file_path

    def _move_track_to_done_folder(self):
        directory = os.path.dirname(self.file_path)
        done_folder_path = os.path.join(directory, DONE_FOLDER_NAME)
        if not os.path.exists(done_folder_path):
            os.makedirs(done_folder_path)
        file_name = os.path.basename(self.file_path)
        new_file_path = os.path.join(done_folder_path, file_name)
        shutil.move(self.file_path, new_file_path)
        return file_name
