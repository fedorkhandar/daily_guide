import configparser
import logging

config = configparser.ConfigParser()
config.read("config/config.ini")
module_logger = logging.getLogger(config["logger"]["rootname"] + "." + __name__)

def calc_smth():
    module_logger.error("calc_smth: x")
    module_logger.warning("calc_smth: x")
    module_logger.info("calc_smth: x")
    module_logger.debug("calc_smth: x")
    pass