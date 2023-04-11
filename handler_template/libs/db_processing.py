import asyncio
import asyncpg
import configparser
from typing import List

import mylogging

config = configparser.ConfigParser()
config.read("config/config.ini")
module_logger = mylogging.set_logger(config, __name__)

async def execute_query(conn_pool: asyncpg.pool.Pool, query: str):
    module_logger.debug("execute_query: '%s'", query)

    result = None

    try:
        async with conn_pool.acquire() as conn:
            result = await conn.execute(query)

    except Exception as E:
        module_logger.error("%s: %s", E, query)

    return result
    
async def execute_transaction_queries(
        conn_pool: asyncpg.pool.Pool, 
        queries: List[str]
    ):
    module_logger.debug("execute_queries")
    for query in queries:
        module_logger.debug("'%s'", query)

    result = None

    try:
        async with conn_pool.acquire() as conn:
            async with conn.transaction():
                for query in queries:
                    result = await conn.execute(query)

    except Exception as E:
        module_logger.error("%s: %s", E, ", ".join(queries))

    return result
    
async def insert_many(conn_pool, table, cols, rows, returning_flag=False):
    statement = f"INSERT INTO {table} (cols) VALUES ($1, $2, $3);"
    await conn_pool.executemany(statement, rows)


