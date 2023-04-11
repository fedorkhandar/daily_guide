import asyncpg
import configparser

from dataclasses import dataclass
from typing import Dict

@dataclass
class shared_data:
    # NO config: configparser.ConfigParser 
    # connection
    # conn_settings: Dict[str, str] = None
    conn_pool: asyncpg.pool.Pool = None
    sch: str = None
    data_fname: str = None
    
    #other_data
    async def init(self, config):
        self.conn_pool = await asyncpg.create_pool(
            host=config['db']['host'],
            port=int(config['db']['port']),
            user=config['db']['user'],
            password=config['db']['password'],
            database=config['db']['database'],
            ssl=config['db']['ssl'],
            min_size=1,
            max_size=8
        )
        self.sch = 'example_schema'
        self.data_fname = "example.txt"
        
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(shared_data, cls).__new__(cls)
        return cls.instance

