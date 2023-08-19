import os
from urllib.request import urlopen

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

from enums import ID3Metadata, TrackInfo


class MetadataManager:
    @staticmethod
    def extract_metadata(file_path):
        audio = EasyID3(file_path)
        artist = audio.get(ID3Metadata.ARTIST.value, [None])[0]
        title = audio.get(ID3Metadata.TITLE.value, [None])[0]
        return artist, title

    def update_metadata(self, file_path, track):
        audio = EasyID3(file_path)
        print("bbbbbbbbbbbbbbb")
        print(track)
        try:
            audio.add_tags()
        except Exception:
            pass
        audio[ID3Metadata.ARTIST.value] = track[TrackInfo.ARTISTS.value]
        audio[ID3Metadata.TITLE.value] = track[TrackInfo.TITLE.value]
        audio[ID3Metadata.ALBUM.value] = track[TrackInfo.ALBUM.value]
        audio[ID3Metadata.DATE.value] = str(track[TrackInfo.DATE.value]) if track[
                                                                                TrackInfo.DATE.value] is not None else ''
        audio[ID3Metadata.GENRE.value] = track[TrackInfo.GENRE.value]
        audio[ID3Metadata.ORGANIZATION.value] = track[TrackInfo.LABEL.value]
        audio[ID3Metadata.TRACK_NUMBER.value] = str(track[TrackInfo.TRACK_NUMBER.value])
        audio[ID3Metadata.BPM.value] = str(track[TrackInfo.BPM.value])
        audio[ID3Metadata.TKEY.value] = track[TrackInfo.KEY.value]

        audio.save()

        self._update_artwork(file_path, track[TrackInfo.ARTWORK.value])

    @staticmethod
    def delete_metadata(file_path):
        print('Delete metadata')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File does not exist: {file_path}')
        audio = EasyID3(file_path)
        audio.delete()
        audio.save()

    @staticmethod
    def _update_artwork(file_path, artwork_url):
        print('Update artwork')
        audio = MP3(file_path, ID3=ID3)

        try:
            audio.add_tags()
        except Exception:
            pass

        if ID3Metadata.APIC.value in audio.tags:
            del (audio.tags[ID3Metadata.APIC.value])

        image_data = urlopen(artwork_url).read()

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
