import logging
import inspect


class LoggerManager:
    def __init__(self, active_logs=True):
        self.active_logs = active_logs
        self._setup_logger()

    def _setup_logger(self):
        caller_frame = inspect.stack()[2]  # Cambiar índice a [2]
        caller_file = caller_frame.filename
        caller_file_name = caller_file[caller_file.rfind("/") + 1:caller_file.find(".py")]

        if self.active_logs:
            logging.basicConfig(
                level=logging.DEBUG,
                # filename=f"{caller_file_name}.log",  # Usar el archivo del invocador
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