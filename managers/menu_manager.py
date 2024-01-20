import time

from constants import SQLITE_DB_PATH, MENU_CHOICE_1, MENU_CHOICE_2, VALIDATE_KEY, DECLINE_KEY, EXIT_KEY, JSON_PLAYLIST_PATH
from enums import TrackInfo, PlaylistType, MenuAction
from loggers import TrackProcessingLog, AppLogger
from processors.playlist_processor import PlaylistProcessor
from processors.track_processor import TrackProcessor


class MenuManager:
    def __init__(self):
        self.logger = AppLogger().get_logger()
        self.current_choice = None
        self.main_menu_text = "###MENU###\n1: Move Tracks From Playlist\n2: Process Tracks"
        self.playlist_menu_text = "###PLAYLIST FORMAT###\n1: SQLITE\n2: JSON"

    def display_main_menu(self):
        main_menu_choices = {MENU_CHOICE_1: MenuAction.PROCESS_PLAYLIST.value,
                             MENU_CHOICE_2: MenuAction.PROCESS_TRACKS.value}
        choice, action = self._get_user_choice(self.main_menu_text, main_menu_choices)
        if choice is None:
            return
        elif action == MenuAction.PROCESS_PLAYLIST.value:
            self._display_playlist_menu()
        elif action == MenuAction.PROCESS_TRACKS.value:
            self._process_tracks()

    @staticmethod
    def confirmation_track_processor_menu(best_match, artist, title, logger):
        while True:
            time.sleep(0.1)
            user_input = input(
                f'Replace file: {artist} - {title}, with: {best_match[TrackInfo.ARTISTS.value]} - {best_match[TrackInfo.TITLE.value]} ({VALIDATE_KEY}/{DECLINE_KEY})\n').lower()
            if user_input in [VALIDATE_KEY, DECLINE_KEY]:
                return user_input
            else:
                logger.info(f'Invalid input. Please enter {VALIDATE_KEY} or {DECLINE_KEY}.')

    def _get_user_choice(self, menu_text, valid_choices):
        while True:
            time.sleep(0.1)
            print(menu_text)
            choice = input(f'Enter your choice (or type "{EXIT_KEY}" to quit): ')
            if choice.lower() == EXIT_KEY:
                return None, None
            if choice in valid_choices:
                return choice, valid_choices[choice]
            self.logger.info(f'Invalid choice. Please enter a valid option or {EXIT_KEY} to quit.')

    def _display_playlist_menu(self):
        playlist_menu_choices = {MENU_CHOICE_1: (PlaylistType.SQLITE.value, SQLITE_DB_PATH),
                                 MENU_CHOICE_2: (PlaylistType.JSON.value, JSON_PLAYLIST_PATH)}
        choice, action = self._get_user_choice(self.playlist_menu_text, playlist_menu_choices)
        if choice is not None:
            playlist_type, playlist_path = action
            self._process_playlist(playlist_type, playlist_path)

    def _process_playlist(self, playlist_type, playlist_path):
        playlist_processor = PlaylistProcessor(playlist_type, playlist_path)
        try:
            self.logger.info('###START PLAYLIST PROCESSING###')
            playlist_processor.run()
        except Exception as e:
            self.logger.error(f'An error occurred while processing the playlist: {e}')
        finally:
            if len(playlist_processor.tracks_in_success) > 0 or len(playlist_processor.tracks_in_failure) > 0:
                self._handle_logs(playlist_processor)
            self.logger.info('###END PLAYLIST PROCESSING###')

    def _process_tracks(self):
        track_processor = TrackProcessor()
        try:
            self.logger.info('###START TRACKS PROCESSING###')
            track_processor.run()
        except Exception as e:
            self.logger.error(f'An error occurred while processing the tracks: {e}')
        finally:
            if len(track_processor.tracks_in_success) > 0 or len(track_processor.tracks_in_failure) > 0:
                self._handle_logs(track_processor)
            self.logger.info('###END TRACKS PROCESSING###')

    def _handle_logs(self, processor):
        if len(processor.tracks_in_success) > 0 or len(processor.tracks_in_failure) > 0:
            self.logger.info('Writing logs')
            processing_log = TrackProcessingLog(processor.tracks_in_success, processor.tracks_in_failure,
                                                processor.total_tracks)
            processing_log.write_log()
            processing_log.open_log_file()
        else:
            self.logger.warning('No tracks to process !')
