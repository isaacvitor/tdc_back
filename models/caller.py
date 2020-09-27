import peewee
from datetime import datetime
from models.base import BaseModel

# Disclaimer #
# To simplify I put the phone number as a Caller's property 
# of course a Caller could have a lot of phone numbers. one => many
class Caller(BaseModel):
    id = peewee.AutoField()
    phone_number = peewee.CharField(max_length=10)

class Agent(Caller):
    id = peewee.AutoField()
    phone_number = peewee.CharField(max_length=10)