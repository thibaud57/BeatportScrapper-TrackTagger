import time

from constants import INVALID_CHARS
from enums import TrackInfo
from loggers import AppLogger


def get_user_input(best_match, artist, title):
    logger = AppLogger().get_logger()
    while True:
        time.sleep(0.1)
        user_input = input(
            f'Replace file: {artist} - {title}, by: {best_match[TrackInfo.ARTISTS.value]} - {best_match[TrackInfo.TITLE.value]} (Y/N)\n').lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            logger.info('Invalid input. Please enter Y or N.')


def clean_filename(filename):
    for char in INVALID_CHARS:
        filename = filename.replace(char, '')
    return filename
