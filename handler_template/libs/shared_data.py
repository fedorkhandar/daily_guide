import asyncpg
import configparser

from dataclasses import dataclass
from typing import Dict, Union
import db

@dataclass
class shared_data:
    # connection
    conn_settings: Dict[str, str] = None
    dbase: db.Database = None
    # sch: str = None
    data_fname: str = None
    
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
        # self.sch = 'example_schema'
        self.data_fname = "example.txt"
        
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(shared_data, cls).__new__(cls)
        return cls.instance

