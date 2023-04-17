"""
web responses processing
"""
import codecs
import configparser
import json
from aiohttp import web
import mylogging
import shared_data

config = configparser.ConfigParser()
config.read("config/config.ini")
module_logger = mylogging.set_logger(config,  __name__)


async def jr400(error_message):
    """
    response 400 forming
    """
    module_logger.debug("jr400: %s", error_message)
    return web.json_response({
        "status": 400,
        "text": error_message,
        "content_type": "text/html",
        "charset": "utf-8",
    })
    
async def jr200(data):
    """
    response 200 forming
    """
    module_logger.debug("jr200: %s", str(data))
    return web.json_response(
        data, 
        status=200, 
        content_type="application/json", 
        dumps=json.dumps
    )

async def save_failed(save_flag, folder, xml_data):
    """
    saves failed data if save_flag=="1"
    """
    module_logger.debug("save_failed: save_flag=%s: data[%i] to '%s'", save_flag, len(xml_data), folder)
    if save_flag == "1":
        fname = f"{folder}/_1.xml"
        with codecs.open(fname, "w", "utf-8") as fout:
            print(xml_data, file=fout)