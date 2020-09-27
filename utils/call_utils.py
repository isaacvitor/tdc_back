from enum import Enum
from random import randint
from math import ceil
from datetime import date, datetime, timedelta


# ENUM to CallType #
class CallType(str, Enum):
    INBOUND = 'INBOUND'
    OUTBOUND = 'OUTBOUND'

def calculate_duration(started_time:datetime, finished_time:datetime):
        delta:timedelta = finished_time - started_time
        #Convert delta to minutes
        return ceil(delta.total_seconds() / 60 )

def create_fake_phone_number():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(randint(10**9, 10**10-1))
    return int(n[:3] + '' + n[3:6] + '' + n[6:])

def create_phone_numbers(quantity:int):
    numbers:list = []
    for i in range(quantity):
        numbers.append(create_fake_phone_number())
    return numbers


def create_fake_calls(call_type:CallType, agents_phones:list, clients_phones:list, day:date = date.today(), 
    quantity:int = 1, min_duration:int = 5, max_duration:int = 60):
    calls:list = []
    max_agents = len(agents_phones) - 1
    max_clients = len(agents_phones) - 1

    for i in range(quantity):
        fake_call:dict = {}
        fake_call['call_type'] = call_type
        fake_call['day'] = day

        # INBOUND CALL
        if call_type == CallType.INBOUND:
            fake_call['caller'] = clients_phones[randint(0,max_clients)]
            fake_call['callee'] = agents_phones[randint(0,max_agents)]
        else:
            fake_call['caller'] = agents_phones[randint(0,max_agents)]
            fake_call['callee'] = clients_phones[randint(0,max_clients)]
        
        now = datetime.utcnow()
        fake_call['started'] = now
        fake_call['finished'] = now + timedelta(minutes=randint(min_duration, max_duration))
        fake_call['duration'] = calculate_duration(fake_call['started'], fake_call['finished'])
        calls.append(fake_call)

    return calls

