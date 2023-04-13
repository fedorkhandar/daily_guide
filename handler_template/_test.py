import asyncio
import base64
import codecs
import configparser
import json
import sys
import time

from aiohttp import web

sys.path.insert(1, 'libs')
import mylogging
import shared_data

config = configparser.ConfigParser()
config.read("config/config.ini")
logger = mylogging.set_logger(config)

async def test():
    app_data = shared_data.shared_data()
    await app_data.init(config)
    
    table = 'example'
    col_desc = {
        'example_id':'SERIAL PRIMARY KEY',
        'example_int':'INT',
        'example_varchar':'VARCHAR',
        'example_text':'TEXT',
        'example_created_at':'TIMESTAMP NOT NULL DEFAULT NOW()'
    }
    cols = [key for key, value in col_desc.items() if not value in ['SERIAL PRIMARY KEY', 'TIMESTAMP NOT NULL DEFAULT NOW()']]
    rows = [[i, f"varchar{i}", f"text{i}"] for i in range(100)]
    
    await app_data.dbase.start_db(table, col_desc)
    start = time.time()
    returning_ids = await app_data.dbase.insert_many(table, cols, rows, 'example_id')
    a = time.time() - start
    
    start = time.time()
    await app_data.dbase.insert_many(table, cols, rows)
    b = time.time() - start

    result = await app_data.dbase.update(
        "example", 
        data=[
            {"col":"example_text", "row": "new_text"},
            {"col":"example_int", "row":64}
        ],
        where=[
            {"col":"example_id", "sgn": "<", "row": 10},
            {"col":"example_id","sgn":">","row":4}
        ]
    )
    print(result)
    
    result = await app_data.dbase.select(
        "example", 
        cols=["example_id", "example_text"],
        where=[
            {"col":"example_id", "sgn": "<", "row": 12},
            {"col":"example_id","sgn":">","row":0}
        ],
        order_by="example_id",
        sort_dir="ASC"
    )
    print(result)
    
asyncio.run(test())
