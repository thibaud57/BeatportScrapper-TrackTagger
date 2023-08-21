import time

from constants import INVALID_FILENAME_CHARS, ORIGINAL_MIX
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
    for char in INVALID_FILENAME_CHARS:
        filename = filename.replace(char, '')
    return filename


def clean_artist(artist):
    if ';' in artist:
        artists = artist.split(';')
        artists = [a.strip() for a in artists if a.strip()]
        artist = ', '.join(artists)
    return artist


def add_original_name_to_title_if_needed(title):
    if title.find('(') == -1 and title.find(')') == -1:
        title += ORIGINAL_MIX
    return title
