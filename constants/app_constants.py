MAX_RETRIES = 3
SCRIPT_ID = '__NEXT_DATA__'
BEATPORT_SEARCH_URL = 'https://www.beatport.com/search?q='
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
INVALID_FILENAME_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
VALIDATE_KEY = 'y'
DECLINE_KEY = 'n'
EXIT_KEY = 'e'
MENU_CHOICE_1 = '1'
MENU_CHOICE_2 = '2'
MENU_CHOICE_3 = '3'
THREADS_NUMBER = 5
SQLITE_QUERY_PATH = 'ressources/SQLitePlaylistQuerry.sql'
SQLITE_DB_PATH = r"D:\Desktop\vlc_media.db"  # Update this to the path of your SQLite database file
JSON_PLAYLIST_PATH = r"D:\Desktop\delete.json"  # Update this to the path of your JSON file
TEXT_PLAYLIST_PATH = r"D:\Desktop\Delete.txt"  # Update this to the path of your TEXT file
ARTIST_TEXT_KEY = 'Artiste'  # Can be replaced with the value of the artist key in your text file
TRACK_TITLE_TEXT_KEY = 'Titre du morceau'  # Cafzn be replaced with the value of the track title key in your text file
LOCATION_TEXT_KEY = 'Emplacement'  # Can be replaced with the value of the location key in your text file
ORIGINAL_TRACKS_FILE_PATH = r'D:\Downloads\Mars\\'  # Update this to the directory where your tracks are initially located before being moved by the playlist
PROCESSING_TRACKS_FILE_PATH = r'D:\Music\Rename\\'  # Update this to the directory where your tracks are stored for processing
DONE_FOLDER_NAME = 'done'  # Can be replaced with the desired folder name
MATCHING_SCORE_LIMIT = 90
ARTIST_SCORE_LIMIT = 70
TITLE_SCORE_LIMIT = 70
'''
Determines the threshold for matching accuracy. 
A value of 0 makes the matching algorithm very lenient, allowing almost any result to be considered a match. 
On the other hand, a value of 100 makes the algorithm very strict, only considering results that are an exact match. 
Adjust this value between 0 and 100 based on your desired level of matching accuracy.
'''

# exemple: 'F:\Téléchargements\\Decembre\\'
# D:\DJ