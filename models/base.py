import peewee
from datetime import datetime
from playhouse.sqlite_ext import SqliteExtDatabase
from os import getenv

DATABASE_PATH = getenv('TDC_DATABASE_PATH')
tdc_db = SqliteExtDatabase(DATABASE_PATH, pragmas={'foreign_keys': 1})

class BaseModel(peewee.Model):
    class Meta:
        database = tdc_db
    
