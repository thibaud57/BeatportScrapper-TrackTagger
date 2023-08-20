MAX_RETRIES = 3
SCRIPT_ID = '__NEXT_DATA__'
BEATPORT_SEARCH_URL = 'https://www.beatport.com/search?q='
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
CHROME_DRIVER = './chromedriver.exe'
ORIGINAL_MIX = ' (original mix)'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
VALIDATE_KEY = 'y'
DONE_FOLDER_NAME = 'done'  # Can be replaced with the desired folder name
TRACKS_FILE_PATH = 'D:\Rename\\'  # Replace with your preferred file path
MATCHING_SCORE_LIMIT = 70
'''
Determines the threshold for matching accuracy. 
A value of 0 makes the matching algorithm very lenient, allowing almost any result to be considered a match. 
On the other hand, a value of 100 makes the algorithm very strict, only considering results that are an exact match. 
Adjust this value between 0 and 100 based on your desired level of matching accuracy.
'''
