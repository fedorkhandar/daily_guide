import asyncio
import base64
import codecs
import configparser
import json
import sys

from aiohttp import web

sys.path.insert(1, 'lib')
import mylogging
import shared_data

config = configparser.ConfigParser()
config.read("config/config.ini")
logger = mylogging.set_logger(config)

async def json_response400(error_message):
    """
    response 400 forming
    """
    return web.json_response({
        "status": 400,
        "text": error_message,
        "content_type": "text/html",
        "charset": "utf-8",
    })
    
async def json_response200(data):
    """
    response 200 forming
    """
    return web.json_response(
        data, 
        status=200, 
        content_type="application/json", 
        dumps=json.dumps
    )

async def save_failed(save_flag, folder, xml_id, xml_data):
    """
    saves failed data if save_flag=="1"
    """
    if save_flag == "1":
        fname = f"{folder}/{xml_id}.xml"
        with codecs.open(fname, "w", "utf-8") as fout:
            print(xml_data, file=fout)

async def processing(xml_id, xml_data):
    """
    some data processing
    """
    response = {
        "result":"ok",
        "error_code":0,
        "error_message":"none",
        "data":xml_data
    }
    return response
    
async def handler(request):
    """
    request handler -- calls processing
    """
    # read id
    try:
        reader = await request.json()
        xml_id = reader["id"]
        logger.info("succeed reading 'id' from json: %s", xml_id)
    except Exception as error:
        logger.error("failed reading 'id' from json: %s", error)
        return await json_response400("failed reading 'id' from json")

    # read data
    try:
        xml_data = ''
        if config['server']['is_xml_b64'] == 1:
            xml_data = base64.b64decode(reader["data"]).decode("utf-8")
        else:
            xml_data = reader["data"]
            
        logger.info("succeed reading 'data' from json: %s", xml_id)
    except Exception as error:
        await save_failed(
            config["failed"]["save_flag"],
            config["failed"]["folder"],
            xml_id,
            xml_data,
        )
        logger.error("failed reading 'data' from json: %s", error)
        return await json_response400("failed reading 'data' from json")
    
    # processing id and data
    try:
        data = await processing(xml_id, xml_data)
        logger.info("succeed processing XML: %s", xml_id)
        return await json_response200(data)
    except Exception as error:
        await save_failed(
            config["failed"]["save_flag"],
            config["failed"]["folder"],
            xml_id,
            xml_data,
        )
        logger.error("failed processing XML: %s, %s", xml_id, error)
        return await json_response400("failed processing xml file")

async def config_once_init(app):
    app['app_data'] = shared_data.shared_data()
    await app['app_data'].init(config)

# handler
 # pool = request.app['pool']
 # async with pool.acquire() as connection:
 
# app start 
 # app['pool'] = await asyncpg.create_pool


def main():
    app = web.Application(client_max_size = int(config["server"]["client_max_size"]))
    app.on_startup.append(config_once_init)
    
    app.add_routes([web.post("/" + config["server"]["path"], handler)])   
    web.run_app(app, port=config["server"]["port"])

if __name__ == "__main__":
    main()