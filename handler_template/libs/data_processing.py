import asyncio
import configparser
import logging

config = configparser.ConfigParser()
config.read("config/config.ini")
module_logger = logging.getLogger(config["logger"]["rootname"] + "." + __name__)

async def processing(input_data):
    check_flag = True
    error_message = "No errors"
    output_data = {"processed": "hihe"}
    return check_flag, error_message, output_data
    