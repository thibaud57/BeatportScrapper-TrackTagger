from typing import re

from constants import INVALID_FILENAME_CHARS
from enums import TitleType


def clean_filename(filename):
    pattern = f"([{''.join(INVALID_FILENAME_CHARS)}])\s*|\s*([{''.join(INVALID_FILENAME_CHARS)}])"
    cleaned_filename = re.sub(pattern, ' ', filename)
    cleaned_filename = re.sub(' +', ' ', cleaned_filename)
    return cleaned_filename.strip()


def clean_artist(artist):
    if ';' in artist:
        artists = artist.split(';')
        artists = [a.strip() for a in artists if a.strip()]
        artist = ', '.join(artists)
    return artist


def add_original_name_to_title_if_needed(title):
    if title.find('(') == -1 and title.find(')') == -1:
        title += f'({TitleType.ORIGINAL_MIX.value})'
    return title
