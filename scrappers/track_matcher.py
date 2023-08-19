from datetime import datetime

from fuzzywuzzy import fuzz

from constants import ORIGINAL_MIX, DATE_FORMAT, MATCHING_SCORE_LIMIT
from enums import ArtistType, TrackInfo, BeatportField


class TrackMatcher:
    def parse_track_info(self, data):
        if data is None:
            return None

        if not isinstance(data, dict):
            raise TypeError('Data must be a dict.')

        tracks = data.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [{}])[0].get(
            'state',
            {}).get(
            'data', {}).get('tracks', {}).get('data', [])

        if tracks:
            return [self._extract_track_info(track) for track in tracks]
        else:
            return None

    def _extract_track_info(self, track):
        return {
            TrackInfo.ARTISTS.value: self._extract_artists(track),
            TrackInfo.TITLE.value: self._extract_title(track),
            TrackInfo.GENRE.value: track.get(BeatportField.GENRE.value, {})[0].get(BeatportField.GENRE_NAME.value, ''),
            TrackInfo.LABEL.value: track.get(BeatportField.LABEL.value, {}).get(BeatportField.LABEL_NAME.value, ''),
            TrackInfo.DATE.value: datetime.strptime(track.get(BeatportField.RELEASE_DATE.value, ''), DATE_FORMAT).year,
            TrackInfo.ALBUM.value: track.get(BeatportField.RELEASE.value, {}).get(BeatportField.RELEASE_NAME.value, ''),
            TrackInfo.ARTWORK.value: track.get(BeatportField.RELEASE.value, {}).get(
                BeatportField.RELEASE_IMAGE_URI.value, ''),
        }

    @staticmethod
    def _extract_artists(track):
        artists = track.get(BeatportField.ARTISTS.value, [])
        filtered_artists = [
            artist.get(BeatportField.ARTIST_NAME.value, '')
            for artist in artists
            if artist.get(BeatportField.ARTIST_TYPE_NAME.value) != ArtistType.REMIXER.value
        ]
        return ', '.join(filtered_artists)

    @staticmethod
    def _extract_title(track):
        track_name = track.get(BeatportField.TRACK_NAME.value, '')
        mix_name = track.get(BeatportField.MIX_NAME.value, '')
        if mix_name in track_name:
            return track_name
        else:
            return f'{track_name} ({mix_name})'

    @staticmethod
    def find_best_match(artist, title, json_data_list):
        csv_artist = artist.lower().replace('_', ' ')
        csv_title = title.lower().replace('_', ' ')

        if csv_title.find('(') == -1 and csv_title.find(')') == -1:
            csv_title += ORIGINAL_MIX

        max_score = -1
        best_match = None

        for json_data in json_data_list:
            artist_score = fuzz.token_set_ratio(csv_artist, json_data[TrackInfo.ARTISTS.value].lower())
            title_score = fuzz.token_set_ratio(csv_title, json_data[TrackInfo.TITLE.value].lower())

            if artist_score >= MATCHING_SCORE_LIMIT and title_score >= MATCHING_SCORE_LIMIT:
                total_score = artist_score + title_score

                if total_score > max_score:
                    max_score = total_score
                    best_match = json_data

        if best_match is not None:
            return best_match, max_score / 2

        return None, -1
