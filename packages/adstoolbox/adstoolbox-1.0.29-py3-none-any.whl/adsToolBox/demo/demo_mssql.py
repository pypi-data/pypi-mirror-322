from adsToolBox.logger import Logger
from adsToolBox.loadEnv import env
from adsToolBox.global_config import set_timer
from adsToolBox.dbMssql import dbMssql

logger = Logger(Logger.DEBUG, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')
set_timer(True)

connection = dbMssql({
    "database": env.MSSQL_DWH_DB,
    "user": env.MSSQL_DWH_USER,
    "password": env.MSSQL_DWH_PWD,
    "host": env.MSSQL_DWH_HOST,
    "package": "pymssql"
}, logger, 10_000)
connection.connect()

connection.sqlExec('''
IF OBJECT_ID('dbo.insert_test', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test;
CREATE TABLE dbo.insert_test (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    age INT
);''')

cols = ["name", "email", "age"]
rows = [[f"nom_{i}", f"émail_{i}", i] for i in range(1, 10_001)]
result = connection.insertBulk('dbo', 'insert_test', cols, rows)
print(f"Insert: {result}")

cols = ['name', 'email', 'age']
rows = [[f'nom_{i}', 'UPSERT', 10_000] for i in range(5_000, 12_001)]
result = connection.upsertBulk('dbo', 'insert_test', cols, rows, ['name'])
print(f"Upsert: {result}")