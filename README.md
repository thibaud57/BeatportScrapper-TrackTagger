# BeatportScrapperTrackTagger

## Description

This project allows you to automatically update the tags of your music tracks by scraping data from the Beatport
website. Additionally, it includes a feature to extract playlist data and move tracks between folders.

## Configuration

### Installation

Before diving into the usage, ensure you have all the necessary dependencies installed. Execute the following command to
install them:

```bash
pip install -r requirements.txt
```

### `constants` Directory

Inside the `constants` directory, you'll find the `app_constants.py` file. This file contains several constants that you
can customize to your needs:

- **SQLITE_DB_PATH**: The default location is <your_sql_db_path>. Update this to the path of your SQLite database
  file.
- **JSON_PLAYLIST_PATH**: The default location is <your_json_playlist_path>. Update this to the path of your JSON
  playlist
  file.
- **TEXT_PLAYLIST_PATH**: The default location is <your_text_playlist_path>. Update this to the path of your TEXT
  playlist
  file. You can easily export your playlist into a text file from Rekordbox.


- **ORIGINAL_TRACKS_FILE_PATH**: The default location is <your_original_tracks_folder>. Update this to the directory
  where your
  tracks are initially located before being moved by the playlist.  
  Note: Subfolders are supported for this feature.
- **PROCESSING_TRACKS_FILE_PATH**: Default location is <your_final_tracks_folder>. Update this to the directory where
  your tracks are
  stored.  
  Note: Subfolders are not supported yet for this feature.
- **DONE_FOLDER_NAME**: Default name is 'done'. Change this if you prefer a different name for your final folder.


- **ARTIST_TEXT_KEY**: This refers to the name of the artist key in the header of your text file. For example, if you
  export from Rekordbox in French, it would be "Artiste".
- **TRACK_TITLE_TEXT_KEY**: This refers to the name of the track title key in the header of your text file. In French,
  it would be "Titre du morceau".
- **LOCATION_TEXT_KEY**: This refers to the name of the location key in the header of your text file. In French, it
  would be "Emplacement".


- **ARTIST_SCORE_LIMIT**: This sets the minimum score required for artist name matching. The score must be between 0 and 100.
- **TITLE_SCORE_LIMIT**: This sets the minimum score required for title matching. The score must be between 0 and 100.
- **MATCHING_SCORE_LIMIT**: This determines the matching algorithm's accuracy threshold. A value of 0 is lenient,
  considering almost any result a match, while a value of 100 is strict, requiring an exact match. Adjust between 0 and
  100 to suit your accuracy preference.

## How to Use

Start by running the main project with the command:

```bash
python main.py
```

## Menu Options

Upon running the main project, you'll be presented with a menu:

1. **Move Tracks From Playlist**: This option allows you to move tracks from a specifier playlist to a done folder.
2. **Process Tracks**: This option will proceed to update the tags of your music tracks.

Select the appropriate option based on your needs.

### Extract Playlist

1. Extract your playlist data and move files to a specified folder.
   Options: Select the option that matches the format of your playlist.
    1. SQLITE format (i.e., VLC) -> point the `SQLITE_DB_PATH` constant to it.
    2. JSON format -> point the `JSON_PLAYLIST_PATH` constant to it.
    3. TEXT format -> point the `TEXT_PLAYLIST_PATH` constant to it.
       Note: You can export a playlist from Rekordbox into text. Ensure that the exported file includes the following columns: Artist, Track title, Location. The text file should be formatted as follows:
   ```text
   # Artist Track Title Genre	BPM	Key	Time Year Label Date Added Location
   1. Artist name, Track title, Techno, 140, 3B, 05:00, 2024, Label, 2023-12-06, C:/MyDjFolder/track.mp3
    ```
2. Select your `ORIGINAL_TRACKS_FILE_PATH` where all your tracks are located.  
   Note: Subfolders are supported for this feature.
3. Wait until the end of the program. Tracks are moved to `PROCESSING_TRACKS_FILE_PATH \ DONE_FOLDER_NAME`.

Upon completion, a log file is generated in the `DONE_FOLDER_NAME` directory, detailing the moved music tracks.

### Process Tracks

1. Create a directory containing all the music tracks you intend to replace tags and rename. Point it to
   the `PROCESSING_TRACKS_FILE_PATH` constant.  
   Note: Subfolders are not supported yet for this feature.
2. Wait until the end of the program. Updated tracks are moved to `PROCESSING_TRACKS_FILE_PATH \ DONE_FOLDER_NAME`.

Note: The integrated algorithm evaluates the similarity between your music track and the results from Beatport to ensure
accurate tagging. The `MATCHING_SCORE_LIMIT` constant lets you tweak the algorithm's strictness. If the algorithm
identifies a near match, you'll be prompted to confirm the choice using the `VALIDATE_KEY`.

Upon completion, a log file is generated in the `DONE_FOLDER_NAME` directory, detailing the renamed music tracks.

## Contributing

Interested in enhancing this project? Feel free to submit a pull request!
