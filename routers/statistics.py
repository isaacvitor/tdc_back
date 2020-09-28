from fastapi import APIRouter, HTTPException
from controllers.statistics import StatisticsController
from datetime import date

router = APIRouter()

@router.get(
    '/',
    summary='Get aggregation data',
    description='This endpoint will provide a condensed data about calls by a day parameter'
)
async def clear_database(day:date = date.today()):
    return StatisticsController.get_call_by_day(day)

# @router.get(
#     '/create_fake_calls',
#     summary='Create fake calls',
#     description='This endpoint will create fake calls records'
# )
# async def create_fake_calls(day:date= date.today(), inbound_quantity:int = 1, outbound_quantity:int = 1, min_duration:int = 5, max_duration:int = 60):
#     return DatabaseUtilities.create_calls( day=day, inbound_quantity = inbound_quantity, 
#         outbound_quantity = outbound_quantity, min_duration = min_duration, max_duration = max_duration)
