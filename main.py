from loggers import SuccessLog, AppLogger
from processors import TrackProcessor

if __name__ == "__main__":
    logger = AppLogger().get_logger()
    processor = TrackProcessor()
    try:
        logger.info('###START###')
        processor.run()
    except Exception as e:
        logger.error(f'An error occurred: {e}')
    finally:
        success_log = SuccessLog(processor.tracks_in_success, processor.tracks_file_path)
        logger.info('\nWriting logs')
        success_log.write_success_log()
        logger.info('\n###END###')
