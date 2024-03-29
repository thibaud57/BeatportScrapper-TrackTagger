import os
import re
from urllib.request import urlopen

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

from enums import ID3Metadata, TrackInfo
from loggers import AppLogger
from utils import clean_artist, clean_filename, add_original_name_to_title_if_needed


class MetadataManager:
    def __init__(self):
        self.logger = AppLogger().get_logger()

    def extract_metadata(self, file_path):
        audio = EasyID3(file_path)
        if audio:
            artist = clean_artist(audio.get(ID3Metadata.ARTIST.value, [None])[0])
            title = audio.get(ID3Metadata.TITLE.value, [None])[0]
            return artist, title
        else:
            return self._extract_from_filename(file_path)

    def update_metadata(self, file_path, track):
        audio = EasyID3(file_path)
        self._set_metadata_tags(audio, track)
        audio.save()
        self._set_artwork(file_path, track[TrackInfo.ARTWORK.value])

    def delete_metadata(self, file_path):
        if not os.path.exists(file_path):
            self.logger.error(f'File does not exist: {file_path}')
        audio = EasyID3(file_path)
        audio.delete()
        audio.save()

    @staticmethod
    def _extract_from_filename(file_path):
        filename = clean_filename(os.path.splitext(os.path.basename(file_path))[0])
        parts = [part.strip() for part in re.split('-', filename)]
        artist = clean_artist(parts[0])
        title = add_original_name_to_title_if_needed(parts[1])
        return artist, title

    @staticmethod
    def _set_metadata_tags(audio, track):
        audio[ID3Metadata.ARTIST.value] = track[TrackInfo.ARTISTS.value]
        audio[ID3Metadata.TITLE.value] = track[TrackInfo.TITLE.value]
        audio[ID3Metadata.ALBUM.value] = track[TrackInfo.ALBUM.value]
        audio[ID3Metadata.DATE.value] = track[TrackInfo.DATE.value]
        audio[ID3Metadata.ORIGINAL_DATE.value] = track[TrackInfo.ORIGINAL_DATE.value]
        audio[ID3Metadata.GENRE.value] = track[TrackInfo.GENRE.value]
        audio[ID3Metadata.ORGANIZATION.value] = track[TrackInfo.LABEL.value]
        audio[ID3Metadata.TRACK_NUMBER.value] = str(track[TrackInfo.TRACK_NUMBER.value])
        audio[ID3Metadata.BPM.value] = str(track[TrackInfo.BPM.value])
        audio[ID3Metadata.ISRC.value] = track[TrackInfo.ISRC.value]

    def _set_artwork(self, file_path, artwork_url):
        audio = MP3(file_path, ID3=ID3)
        if ID3Metadata.APIC.value in audio.tags:
            del audio.tags[ID3Metadata.APIC.value]
        try:
            image_data = urlopen(artwork_url).read()
        except Exception as e:
            self.logger.error(f'Error fetching artwork from URL: {e} \n For track: {file_path}')
            return
        audio.tags.add(
            APIC(
                encoding=3,  # utf-8
                mime='image/jpeg',  # image/jpeg or image/png
                type=3,  # album front cover
                desc='Cover',
                data=image_data
            )
        )
        audio.save()
