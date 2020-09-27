from playhouse.shortcuts import model_to_dict, dict_to_model
from models.base import BaseModel
from models.base import tdc_db
from models.call import CallType, Call
from models.caller import Caller

def to_dict(model:BaseModel):
    return model_to_dict(model)

def to_model(dict):
    return dict_to_model(dict)

def initialize_db():
    tdc_db.connect()
    tdc_db.create_tables([Call], safe = True)
    tdc_db.close()