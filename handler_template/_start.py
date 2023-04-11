import asyncio
import codecs
import configparser
import sys
sys.path.insert(1, 'lib')
import shared_data
import mylogging
import db_processing as dbp

config = configparser.ConfigParser()
config.read("config/config.ini")
logger = mylogging.set_logger(config)

async def start_db(app_data):
    sch = app_data.sch
    
    queries = [
        f"DROP SCHEMA IF EXISTS {sch} CASCADE;",
        f"CREATE SCHEMA {sch};",
        f"CREATE TABLE IF NOT EXISTS {sch}.example (example_id SERIAL PRIMARY KEY, example_text TEXT, example_varchar VARCHAR, example_int INT, example_create_at TIMESTAMP NOT NULL DEFAULT NOW());",
    ]
    await dbp.execute_transaction_queries(app_data.conn_pool, queries)
    
async def start_data(app_data):
    with codecs.open(app_data.data_fname, "r", "utf-8") as fout: 
        rows = fout.readlines()
        
        queries = []
        for r.rstrip() in rows:
            queries.append(
                "INSERT INTO 
            )
    
async def start():
    app_data = shared_data.shared_data()
    await app_data.init(config)
    
    await start_db(app_data)
    await start_data(app_data)

    
if __name__ == "__main__":
    asyncio.run(start())