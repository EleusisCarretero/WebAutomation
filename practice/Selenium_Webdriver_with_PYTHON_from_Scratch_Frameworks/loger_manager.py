import logging
import inspect
import os


class LoggerManager:
    def __init__(self, active_logs=True, default_log_folder="DEFAULT_LOG_FOLDER"):
        self.active_logs = active_logs
        self._setup_logger(default_log_folder)

    def _setup_logger(self, default_log_folder):
        current_file_path  = os.path.abspath(__file__)
        caller_file_name = current_file_path.split("\\")[-1].strip(".py")
        current_dir = os.path.dirname(current_file_path)
        default_log_folder_path = os.path.join(os.path.abspath(os.path.join(current_dir, "..", "..", "..")), default_log_folder)
        
        print(default_log_folder_path)

        if self.active_logs:
            logging.basicConfig(
                level=logging.DEBUG,
                filemode='a',
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(f"{caller_file_name}.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
        logging.getLogger().addHandler(file_handler)

    def get_logger(self, name):
        return logging.getLogger(name)

if __name__ == '__main__':
    # test the logger
    local_logger = LoggerManager(active_logs=True).get_logger("mylogger")
    local_logger.info("Save info")
    local_logger.error("Showing error")