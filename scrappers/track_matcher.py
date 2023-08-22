from datetime import datetime
from typing import re

from fuzzywuzzy import fuzz

from constants import ORIGINAL_MIX, DATE_FORMAT, ARTIST_SCORE_LIMIT, TITLE_SCORE_LIMIT
from enums import ArtistType, TrackInfo, BeatportField, TitleType


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
            TrackInfo.DATE.value: self._extract_date(True, track),
            TrackInfo.ORIGINAL_DATE.value: self._extract_date(False, track),
            TrackInfo.ALBUM.value: track.get(BeatportField.RELEASE.value, {}).get(BeatportField.RELEASE_NAME.value, ''),
            TrackInfo.ARTWORK.value: track.get(BeatportField.RELEASE.value, {}).get(
                BeatportField.RELEASE_IMAGE_URI.value, ''),
            TrackInfo.TRACK_NUMBER.value: track.get(BeatportField.TRACK_NUMBER.value, 0),
            TrackInfo.BPM.value: track.get(BeatportField.BPM.value, 0),
            TrackInfo.ISRC.value: track.get(BeatportField.ISRC.value, ''),
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
    def _extract_date(only_year, track):
        release_date_string = track.get(BeatportField.RELEASE_DATE.value, '')
        if release_date_string:
            original_date = datetime.strptime(release_date_string, DATE_FORMAT)
        else:
            original_date = None
        if original_date:
            if only_year:
                return str(original_date.year)
            return original_date.strftime('%Y-%m-%d')
        return ''

    @staticmethod
    def find_best_match(artist, title, json_data_list):
        max_score = -1
        best_match = None

        for json_data in json_data_list:
            artist_score = fuzz.token_sort_ratio(artist, json_data[TrackInfo.ARTISTS.value].lower())
            title_score = fuzz.ratio(title, json_data[TrackInfo.TITLE.value].lower())

            artist_tokens_diff = len(json_data[TrackInfo.ARTISTS.value].lower().split()) - len(artist.split())
            title_tokens_diff = len(json_data[TrackInfo.TITLE.value].lower().split()) - len(title.split())
            artist_score -= 10 * artist_tokens_diff
            title_score -= 10 * title_tokens_diff

            if TitleType.REMIX.value.lower() in title and TitleType.REMIX.value.lower() not in json_data[TrackInfo.TITLE.value].lower():
                continue

            if artist_score >= ARTIST_SCORE_LIMIT and title_score >= TITLE_SCORE_LIMIT:
                total_score = artist_score + title_score

                if total_score > max_score:
                    max_score = total_score
                    best_match = json_data

        if best_match is not None:
            return best_match, max_score / 2

        return None, -1
