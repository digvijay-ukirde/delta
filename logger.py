import logging

def setup_logger(name: str, log_file: str = None, log_level: int = logging.DEBUG):
    """Sets up a logger that can be used throughout the application."""
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create console handler and set level
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(log_level)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    # logger.addHandler(console_handler)

    if log_file:
        # Optionally, add a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
