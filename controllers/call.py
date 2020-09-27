from datetime import datetime, timedelta
from math import ceil
from config import business_rules
from models import tdc_db, Call, CallType, to_dict


class CallController():

    @staticmethod
    def create(call):
        new_call:dict
        if calls:
            with tdc_db.atomic():                
                # Before use the object spread operator, call_schema(instance of CallSchema) needs to be converted to dict.
                call:dict = call_schema.dict()
                
                #calculating duration
                call['duration'] = CallController.__calculate_duration(call['started'], call['finished'])
                # creating/recording a call
                new_call = Call.create(**call)
        
        return new_call

    @staticmethod
    def create_many(calls):
        new_calls = []
        if calls:
            with tdc_db.atomic():
                for call_schema in calls:
                    # Before use the object spread operator, call_schema(instance of CallSchema) needs to be converted to dict.
                    call:dict = call_schema.dict()
                    
                    #calculating duration
                    call['duration'] = CallController.__calculate_duration(call['started'], call['finished'])
                    
                    new_calls.append(call)
                r = Call.insert_many(new_calls).execute()
        
        return r
    
    @staticmethod
    def list():
        query = Call.select()
        calls:list =  []
        if len(query):
            calls = [to_dict(item) for item in query]
        return calls

    @staticmethod
    def get(call_id:int):
        return Call.get_or_none(id = call_id)

    @staticmethod
    def remove(call_id:int):
        return Call.delete_by_id(call_id)

    
    

    @staticmethod
    def __calculate_duration(started_time:datetime, finished_time:datetime):
        delta:timedelta = finished_time - started_time

        #Convert delta to minutes
        return ceil(delta.total_seconds() / 60 )


