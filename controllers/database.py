from os import getenv
from datetime import date, datetime
from config import business_rules
from routers.calls import CallSchema
from models import tdc_db, initialize_db, models, CallType
from utils.call_utils import create_phone_numbers, create_fake_calls
from controllers.call import CallController

class DatabaseUtilities():

    @staticmethod
    def clear_database():
        # Dropping all models
        tdc_db.drop_tables(models=models)
        # Recreating all models
        initialize_db()
    
    @staticmethod
    def create_calls(day:date = date.today(), inbound_quantity:int = 1, outbound_quantity:int = 1, min_duration:int = 5, max_duration:int = 60):
        max_agents = int(getenv('TDC_MAX_AGENTS')) or business_rules['agents']['max']
        max_clients = int(getenv('TDC_MAX_CLIENTS')) or business_rules['clients']['max']

        agents_phone_numbers:list = create_phone_numbers(max_agents)
        clients_phone_numbers:list = create_phone_numbers(max_clients)

        # Inbound Calls
        inbound_calls = create_fake_calls(CallType.INBOUND, agents_phone_numbers, clients_phone_numbers, 
            day = day, quantity=inbound_quantity, min_duration = min_duration, max_duration = max_duration)
        inbound_calls_schemas = [CallSchema.parse_obj(call) for call in inbound_calls]
        # Outbound
        outbound_calls = create_fake_calls(CallType.OUTBOUND, agents_phone_numbers, clients_phone_numbers,
            day=day, quantity=outbound_quantity, min_duration = min_duration, max_duration = max_duration)
        outbound_calls_schemas = [CallSchema.parse_obj(call) for call in outbound_calls]
        
        in_ret = CallController.create_many(inbound_calls_schemas)
        out_ret = CallController.create_many(outbound_calls_schemas)

        return {"inbound_calls":in_ret, "outbound_calls":out_ret}

    