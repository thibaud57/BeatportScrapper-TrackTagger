from constants import SQLITE_DB_PATH, MENU_CHOICE_1, MENU_CHOICE_2, MENU_EXIT
from enums import TrackInfo
from processors.track_processor import TrackProcessor
from processors.playlist_processor import PlaylistProcessor
from loggers import AppLogger, SuccessLog
import time


class MenuManager:
    def __init__(self):
        self.logger = AppLogger().get_logger()

    def display_main_menu(self):
        while True:
            time.sleep(0.1)
            print("###MENU###")
            print("1. Extract Playlist Data")
            print("2. Process Tracks")
            choice = input("Enter your choice (or type 'exit' to quit): ")
            if choice == MENU_CHOICE_1:
                self._process_playlist()
            elif choice == MENU_CHOICE_2:
                self._process_tracks()
            elif choice.lower() == MENU_EXIT:
                break
            else:
                self.logger.info("Invalid choice. Please enter 1, 2, or 'exit'.")

    def confirmation_track_processor_menu(self, best_match, artist, title):
        while True:
            time.sleep(0.1)
            user_input = input(
                f'Replace file: {artist} - {title}, by: {best_match[TrackInfo.ARTISTS.value]} - {best_match[TrackInfo.TITLE.value]} (Y/N)\n').lower()
            if user_input in ['y', 'n']:
                return user_input
            else:
                self.logger.info('Invalid input. Please enter Y or N.')

    def _process_playlist(self):
        playlist_processor = PlaylistProcessor(SQLITE_DB_PATH)
        try:
            self.logger.info('###START PLAYLIST PROCESSING###')
            playlist_processor.run()
        except Exception as e:
            self.logger.error(f'An error occurred while processing the playlist: {e}')
        finally:
            if len(playlist_processor.tracks_in_success) > 0:
                self._handle_success_logs(playlist_processor)
            self.logger.info('###END PLAYLIST PROCESSING###')

    def _process_tracks(self):
        track_processor = TrackProcessor()
        try:
            self.logger.info('###START TRACKS PROCESSING###')
            track_processor.run()
        except Exception as e:
            self.logger.error(f'An error occurred while processing the tracks: {e}')
        finally:
            if len(track_processor.tracks_in_success) > 0:
                self._handle_success_logs(track_processor)
            self.logger.info('###END TRACKS PROCESSING###')

    def _handle_success_logs(self, processor):
        if len(processor.tracks_in_success) > 0:
            success_log = SuccessLog(processor.tracks_in_success, processor.total_tracks)
            self.logger.info('Writing logs')
            success_log.write_success_log()
            success_log.open_log_file()
        else:
            self.logger.warning('No tracks to process !')
