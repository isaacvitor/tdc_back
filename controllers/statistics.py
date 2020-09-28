from peewee import fn
from datetime import datetime, timedelta
import json

from config import business_rules
from models import tdc_db, Call, CallType, to_dict
from utils.call_utils import calculate_duration, calculate_call_cost, format_timedelta


class StatisticsController():

    @staticmethod
    def get_call_by_day(day):
        calc_rules:dict = {}
        calc_rules['INBOUND'] = business_rules['rates']['inbound']
        calc_rules['OUTBOUND'] = business_rules['rates']['outbound']


        statistics = {
            'total_calls':0,
            'inbound_duration':0, 'outbound_duration':0, 'inbound_duration_str':'', 'outbound_duration_str':'',
            'INBOUND':{'duration':0, 'total':0, 'total_cost':0, 'callers':{}, 'callees':{}, 'calls':[]}, 
            'OUTBOUND':{'duration':0, 'total':0, 'total_cost':0, 'callers':{}, 'callees':{}, 'calls':[]}
        }

        query = ( Call.select(Call).where(Call.day == day) )
        if len(query):
            for call in query:
                # Calculating cost
                fixed_rate =  calc_rules[call.call_type]['fixed_rate'] 
                variable_rate = calc_rules[call.call_type]['variable_rate']
                call_cost =  calculate_call_cost(call.duration,fixed_rate, variable_rate)
                
                #Global
                statistics['total_calls'] = len(query)
                statistics[call.call_type]['duration'] += call.duration
                statistics[call.call_type]['total'] += 1
                statistics[call.call_type]['total_cost'] += call_cost
                
                #Counting by caller 
                caller = str(call.caller)
                if caller in statistics[call.call_type]['callers']:
                    statistics[call.call_type]['callers'][caller] += 1
                else:
                    statistics[call.call_type]['callers'][caller] = 1

                #Counting by callee
                callee = str(call.callee) 
                if callee in statistics[call.call_type]['callees']:
                    statistics[call.call_type]['callees'][callee] += 1
                else:
                    statistics[call.call_type]['callees'][callee] = 1

                #Call Detail
                call_detail = {'total_cost':0}
                call_detail['id'] = call.id
                call_detail['total_cost'] = call_cost
                call_detail['caller'] = call.caller
                call_detail['callee'] = call.callee
                call_detail['duration'] = call.duration
                
                # Appending call detail
                statistics[call.call_type]['calls'].append(call_detail)

            statistics['inbound_duration_str'] = format_timedelta(statistics['INBOUND']['duration'], '{H}:{M}:{S}')
            statistics['outbound_duration_str'] = format_timedelta(statistics['OUTBOUND']['duration'], '{H}:{M}:{S}')
            statistics['inbound_duration'] = statistics['INBOUND']['duration']
            statistics['outbound_duration'] = statistics['OUTBOUND']['duration']

        return statistics

    
    @staticmethod
    def list():
        query = Call.select()
        calls:list =  []
        if len(query):
            calls = [to_dict(item) for item in query]
        return calls



