from enum import Enum


class ID3Metadata(Enum):
    ARTIST = 'artist'
    TITLE = 'title'
    ALBUM = 'album'
    DATE = 'date'
    ORIGINAL_DATE = 'originaldate'
    GENRE = 'genre'
    ORGANIZATION = 'organization'
    APIC = 'APIC:'
    TRACK_NUMBER = 'tracknumber'
    BPM = 'bpm'
    ISRC = 'isrc'
