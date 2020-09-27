import peewee
from datetime import datetime, date
from models.base import BaseModel
from models.caller import Caller
from utils.call_utils import CallType


class Call(BaseModel):
    id = peewee.AutoField()
    day = peewee.DateField(default=date.today())
    # caller = peewee.ForeignKeyField(Caller, backref='from')
    # callee = peewee.ForeignKeyField(Caller, backref='to')
    caller = peewee.IntegerField(null=False)
    callee = peewee.IntegerField(null=False)
    started =  peewee.DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    finished = peewee.DateTimeField(null=False, formats='%Y-%m-%d %H:%M:%S')
    duration = peewee.IntegerField(null=False)
    call_type = peewee.CharField(null=False, default=CallType.INBOUND)


    # def create_inbound_call(self, caller:dict, callee:dict, started:datetime, finished:datetime):
    #     self.create