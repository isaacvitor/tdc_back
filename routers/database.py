from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.delete(
    '/',
    summary='Clear all records',
    description='This endpoint will clear ALL db records'
)
async def clear_data():
    return {'todo':'drop database'}
