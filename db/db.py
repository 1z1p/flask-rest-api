import pymysql
from config import config
 
connect = pymysql.connect(
    host=f'{config["host"]}', 
    user=f'{config["user"]}', 
    password=f'{config["password"]}', 
    database=f'{config["database"]}'
)