import os

from constants import DONE_FOLDER_NAME


class SuccessLog:
    def __init__(self, tracks_in_success, tracks_file_path):
        self.tracks_in_success = tracks_in_success
        self.done_folder_path = os.path.join(tracks_file_path, DONE_FOLDER_NAME)
        self.log_file_path = os.path.join(self.done_folder_path, 'success_log.txt')
        if not os.path.exists(self.done_folder_path):
            os.makedirs(self.done_folder_path)

    def write_success_log(self):
        print('\nWriting logs')
        with open(self.log_file_path, 'w', encoding='utf-8') as log_file:
            log_file.write('Files successfully replaced:\n\n')
            if len(self.tracks_in_success) > 0:
                for old_path, artist, title, new_path in self.tracks_in_success:
                    log_file.write(f'Old path: {old_path}\n')
                    log_file.write(f'With track: {artist} - {title}\n')
                    log_file.write(f'Result is: {new_path}\n\n')
