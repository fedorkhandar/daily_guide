import asyncio
import asyncpg
import os
import time
from typing import Dict
from dataclasses import dataclass

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
        self.pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=8)

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
            
    async def fetch(self):
        pass
        
    async def fetchvalue(self):
        pass
        
    async def fetchvalue(self):
        pass
        
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
        "sch":"example_schema"
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
    rows = [[i, random_string('varchar',i), random_string('text',i)] for i in range(10000)]
    
    await db.start_db(table, col_desc)
    start = time.time()
    returning_ids = await db.insert_many(table, cols, rows, 'example_id')
    a = time.time() - start
    # print(returning_ids)
    
    start = time.time()
    await db.insert_many(table, cols, rows)
    b = time.time() - start
    
    print(a)
    print(b)
    # select_many(table, cols, where, limit, order by, dir=desc/asc)
    # select_one(table, cols, where)
    # count(table, where)
    # update(table, cols, rows, where)
    
if __name__ == "__main__":
    asyncio.run(main())