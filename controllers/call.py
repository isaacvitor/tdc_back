from datetime import datetime, timedelta
from config import business_rules
from models import tdc_db, Call, CallType, to_dict
from utils.call_utils import calculate_duration


class CallController():

    @staticmethod
    def create(call_schema):
        new_call:dict
        if call_schema:
            with tdc_db.atomic():                
                # Before use the object spread operator, call_schema(instance of CallSchema) needs to be converted to dict.
                call:dict = call_schema.dict()
                
                #calculating duration
                call['duration'] = calculate_duration(call['started'], call['finished'])
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
                    call['duration'] = calculate_duration(call['started'], call['finished'])
                    
                    new_calls.append(call)
                r = Call.insert_many(new_calls).execute()
        
        return r
    
    @staticmethod
    def list(page_number:int = 1, itens_per_page:int = 10, call_type:str = None):
        query =( Call
                .select()
                .where(((call_type == None) | ( Call.call_type == call_type)))
                .paginate(page_number, itens_per_page)
                )
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

    


