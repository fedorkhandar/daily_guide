#!/usr/bin/python3
"""
simple web service template
"""
import asyncio
import base64
import codecs
import configparser
import json
import sys

from aiohttp import web

sys.path.insert(1, 'libs')
import myresponse
import mylogging
import shared_data
import data_processing as dp

config = configparser.ConfigParser()
config.read("config/config.ini")
logger = mylogging.set_logger(config)


async def processing(input_data, request_app):
    """
    some data processing
    """
    # operation command 
    if "operation" in input_data:
        if input_data["operation"] == "reload_config":
            await config_once_init(request_app)
    # data processing
    if "data" in input_data:
        return await dp.processing(input_data["data"], request_app['app_data'])
    else:
        check_flag = False
        error_message = "No 'data' in input_data"
        output_data = {}
        return check_flag, error_message, output_data 
    
async def handler(request):
    """
    request handler -- calls processing
    """
    input_data = await request.json()
    check_flag, error_message, output_data = await processing(input_data, request.app)
    if not check_flag:
        await myresponse.save_failed(config["failed"]["save_flag"], config["failed"]["folder"], input_data)
        logger.error("handler: failed processing data: %s", error_message)
    else:
        logger.info("handler: succeed processing data")
        return await myresponse.jr200(output_data)

async def config_once_init(app):
    """
    config_data initialization
    """
    app['app_data'] = shared_data.shared_data()
    await app['app_data'].init(config)

def main():
    """
    main
    """
    app = web.Application(client_max_size = int(config["server"]["client_max_size"]))
    app.on_startup.append(config_once_init)
    app.add_routes([web.post("/" + config["server"]["path"], handler)])   
    web.run_app(app, port=config["server"]["port"])

if __name__ == "__main__":
    main()