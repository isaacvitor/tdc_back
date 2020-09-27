from fastapi import APIRouter, HTTPException
from controllers.database import DatabaseUtilities
from datetime import date

router = APIRouter()

@router.delete(
    '/',
    summary='Clear all records',
    description='**DANGER** - This endpoint will clear ALL database records'
)
async def clear_database():
    return DatabaseUtilities.clear_database()

@router.get(
    '/create_fake_calls',
    summary='Create fake calls',
    description='This endpoint will create fake calls records'
)
async def create_fake_calls(day:date= date.today(), inbound_quantity:int = 1, outbound_quantity:int = 1, min_duration:int = 5, max_duration:int = 60):
    return DatabaseUtilities.create_calls( day=day, inbound_quantity = inbound_quantity, 
        outbound_quantity = outbound_quantity, min_duration = min_duration, max_duration = max_duration)
