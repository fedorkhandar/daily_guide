import asyncio
import asyncpg
import configparser
import os
import time
from typing import Dict
from dataclasses import dataclass
import mylogging

config = configparser.ConfigParser()
config.read("config/config.ini")
module_logger = mylogging.set_logger(config, __name__)

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@dataclass
class Database:
    connection_settings: Dict [str, str]
    dsn: str = None
    pool: asyncpg.pool.Pool = None
    sch: str = None
    
    def __post_init__(self):
        self.dsn = (
            f"postgres://"
            f"{self.connection_settings['user']}:"
            f"{self.connection_settings['password']}@"
            f"{self.connection_settings['host']}:"
            f"{self.connection_settings['port']}/"
            f"{self.connection_settings['database']}?"
            f"{self.connection_settings['option']}"
        )
        if 'sch' in self.connection_settings:
            self.sch = self.connection_settings['sch']
        else:
            self.sch = 'public'
            
    async def init(self):
        self.pool = await asyncpg.create_pool(
            self.dsn, 
            min_size=int(self.connection_settings['min_size']), 
            max_size=int(self.connection_settings['max_size'])
        )



    async def insert_many(self, table, cols, rows, returning_col=None):
        if returning_col is None:
            async with self.pool.acquire() as conn:
                await conn.copy_records_to_table(table, records = rows, columns = cols, schema_name = self.sch)
            return []
        else:
            async with self.pool.acquire() as conn:
                cols_str = ", ".join(cols)
                rows_str = ", ".join(
                    ["(" + ", ".join([f"$${value}$$" for value in row]) + ")" for row in rows]
                )
                query = f"INSERT INTO {self.sch}.{table} ({cols_str}) VALUES {rows_str} RETURNING {returning_col};"
                returning_ids = await conn.fetch(query)
                return [r[returning_col] for r in returning_ids]

    async def execute_query(self, query):
        async with self.pool.acquire() as conn:
            await conn.execute(query)
        
    async def execute_queries(self, queries):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for query in queries:
                    await conn.execute(query)

    async def update(self, table, **kwargs):
        if 'data' in kwargs:
            query = f"UPDATE {self.sch}.{table} SET "
            data_str = ", ".join([f"{x['col']} = $${x['row']}$$" for x in kwargs['data']])
            query += f"{data_str}"
            
            if 'where' in kwargs:
                where_str = " AND ".join([f"{x['col']} {x['sgn']} {x['row']}" for x in kwargs['where']])
                query += f" WHERE {where_str};"
        
            module_logger.debug("update: %s", query)
            async with self.pool.acquire() as conn:
                result = await conn.execute(query)

    async def select(self, table, **kwargs):
        cols_str = "*"
        if 'cols' in kwargs:
            if isinstance(kwargs['cols'], list):
                cols_str = ", ".join(kwargs['cols'])
            else:
                cols_str = kwargs['cols']
        query = f"SELECT {cols_str} FROM {self.sch}.{table}"
        
        if 'where' in kwargs:
            where_str = " AND ".join([f"{x['col']} {x['sgn']} {x['row']}" for x in kwargs['where']])
            query += f" WHERE {where_str}"
        
        if 'order_by' in kwargs:
            query += f" ORDER BY {kwargs['order_by']}"
        
        if 'sort_dir' in kwargs:
            query += f" {kwargs['sort_dir']}"
        
        if 'limit' in kwargs:
            query += f" LIMIT {kwargs['limit']}"
        query += ";"
        
        module_logger.debug("select: %s", query)
        
        async with self.pool.acquire() as conn:
            result = await conn.fetch(query)
        
        
        returning_result = []
        for r in result:
            d = {}
            for key, value in r.items():
                d[key]=value
            returning_result.append(d)
        return returning_result
        
    async def start_db(self, table, col_desc):
        col_data = ",".join([f"{key} {value}" for key, value in col_desc.items()])
        queries = []
        queries.append(f"DROP SCHEMA IF EXISTS {self.sch} CASCADE;")
        queries.append(f"CREATE SCHEMA IF NOT EXISTS {self.sch};")
        queries.append(f"CREATE TABLE IF NOT EXISTS {self.sch}.{table} ({col_data});")
        await self.execute_queries(queries)

def random_string(value, i):
    return f"{value}_{i}"
    
async def main():
    connection_settings = {
        "user":"postgres",
        "database":"postgres",
        "password":"postgres",
        "port":5432,
        "host":"localhost",
        "option":"sslmode=disable",
        "sch":"example_schema",
        "max_size":8,
        "min_size":1
    }
    db = Database(connection_settings)
    await db.init()
    
    table = 'example'
    col_desc = {
        'example_id':'SERIAL PRIMARY KEY',
        'example_int':'INT',
        'example_varchar':'VARCHAR',
        'example_text':'TEXT',
        'example_created_at':'TIMESTAMP NOT NULL DEFAULT NOW()'
    }
    cols = [key for key, value in col_desc.items() if not value in ['SERIAL PRIMARY KEY', 'TIMESTAMP NOT NULL DEFAULT NOW()']]
    rows = [[i, random_string('varchar',i), random_string('text',i)] for i in range(100)]
    
    await db.start_db(table, col_desc)
    start = time.time()
    returning_ids = await db.insert_many(table, cols, rows, 'example_id')
    a = time.time() - start
    
    start = time.time()
    await db.insert_many(table, cols, rows)
    b = time.time() - start

    result = await db.update(
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
    
    # result = await db.select(
        # "example", 
        # cols=["example_id", "example_text", "example_varchar"],
        # where=[
            # {"col":"example_id", "sgn": "<", "row": 10},
            # {"col":"example_int","sgn":">","row":4}
        # ],
        # limit=1
        # # order_by="example_int",
        # # sort_dir="DESC"
    # )
    # print(result)
    # await db.select(
        # "example", 
        # cols="count(*)", 
        # where=[
            # {"col":"example_id", "sgn": "IN", "row": "(1,2,3,4,5,6,7,8,9,10)"}, 
            # {"col":"example_int","sgn":">","row":4}
        # ]
    # )
    
if __name__ == "__main__":
    asyncio.run(main())