import configparser
import sys

sys.path.insert(1, 'lib')
import mylogging
import mylibrary

config = configparser.ConfigParser()
config.read("config/config.ini")

logger = mylogging.set_logger(config)
print(logger)

x = mylibrary.calc_smth()
logger.error("i am in the parser")
logger.warning("i am in the parser")
logger.info("i am in the parser")
logger.debug("i am in the parser")
