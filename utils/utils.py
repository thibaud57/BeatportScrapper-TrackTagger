from enums import TrackInfo


def get_user_input(best_match, best_score, artist, title):
    while True:
        user_input = input(
            f'Replace file: {artist} - {title}, by: {best_match[TrackInfo.ARTISTS.value]} - {best_match[TrackInfo.TITLE.value]} (Y/N)\n').lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            print('Invalid input. Please enter Y or N.')


def clean_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename
