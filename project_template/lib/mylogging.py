import logging
from logging.handlers import RotatingFileHandler

def set_loggers(config):
    s_handler = logging.StreamHandler()
    f_handler = RotatingFileHandler(
        config["logger"]["path_to_logs"], 
        maxBytes=int(config["logger"]["maxbytes"]), 
        backupCount=int(config["logger"]["backupcount"])
    )

    s_format = logging.Formatter(
        "%(name)s - %(levelname)s - %(message)s"
    )
    f_format = logging.Formatter(
        "%(name)s - %(asctime)s - %(message)s"
    )
    s_handler.setFormatter(s_format)
    f_handler.setFormatter(f_format)

    if config["logger"]["show_level"] == "DEBUG":
        s_handler.setLevel(logging.DEBUG)
    elif config["logger"]["show_level"] == "INFO":
        s_handler.setLevel(logging.INFO)
    elif config["logger"]["show_level"] == "WARNING":
        s_handler.setLevel(logging.WARNING)
    else:
        s_handler.setLevel(logging.ERROR)

    if config["logger"]["file_level"] == "DEBUG":
        f_handler.setLevel(logging.DEBUG)
    elif config["logger"]["file_level"] == "INFO":
        f_handler.setLevel(logging.INFO)
    elif config["logger"]["file_level"] == "WARNING":
        f_handler.setLevel(logging.WARNING)
    else:
        f_handler.setLevel(logging.ERROR)
        
    
    return s_handler, f_handler
    
def set_logger(config):
    logger = logging.getLogger(config["logger"]["rootname"])
    if config["logger"]["base_level"] == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif config["logger"]["base_level"] == "INFO":
        logger.setLevel(logging.INFO)
    elif config["logger"]["base_level"] == "WARNING":
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.ERROR)
        
    s_handler, f_handler = set_loggers(config)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)

    return logger