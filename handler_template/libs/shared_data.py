import asyncpg
import codecs
import configparser
import json

from dataclasses import dataclass
from typing import Dict, Union
import db


async def get_pattern(pattern_fname):
    fname = f"data/{pattern_fname}"
    print(fname)
    with codecs.open(fname, "r", "utf-8") as json_file:
        pattern_data = json.load(json_file)
    return pattern_data['pattern']

@dataclass
class shared_data(object):
    # connection
    conn_settings: Dict[str, str] = None
    dbase: db.Database = None
    data_pattern: Dict[str, Union[str, int]] = None
    
    #other_data
    async def init(self, config):
        self.conn_settings = {
            "host":config['db']['host'],
            "port":int(config['db']['port']),
            "user":config['db']['user'],
            "password":config['db']['password'],
            "database":config['db']['database'],
            "min_size":config['db']['min_size'],
            "max_size":config['db']['max_size'],
            "option":config['db']['option'],
            "sch":config['db']['sch'],
        }
        self.dbase = db.Database(self.conn_settings)
        await self.dbase.init()
        self.data_pattern = await get_pattern(config["data"]["pattern_fname"])

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(shared_data, cls).__new__(cls)
        return cls.instance

