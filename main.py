from loggers import SuccessLog
from processors.track_processor import TrackProcessor

if __name__ == "__main__":
    processor = TrackProcessor()
    try:
        print('###START###')
        processor.run()
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        success_log = SuccessLog(processor.tracks_in_success, processor.tracks_file_path)
        success_log.write_success_log()
        print('\n###END###')
