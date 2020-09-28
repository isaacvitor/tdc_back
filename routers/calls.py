from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, date, timedelta
from typing import Optional, List
from pydantic import BaseModel
from utils.call_utils import CallType
from controllers.call import CallController

router = APIRouter()
### CallSchema ###
class CallSchema(BaseModel):
    caller:int
    callee:int
    started:datetime = datetime.now()
    finished:datetime
    duration:int
    call_type:CallType
    day:date = date.today()

### Routers ###

# Create
@router.post(
    "/",
    summary='Create a CALL'
)
async def create(call:CallSchema):
    """
    Create a call registry:

    The call object has the parameters below:
    - **caller**: simple abstraction of the caller's phone number
    - **callee**: simple abstraction of the callee's phone number
    - **started**: when the call started
    - **finished**: when the call finished
    - **duration**: will be calculated by the system, basically is a delta (duration = finished - started) => MINUTES
    - **call_type**: witch kind of call we are creating - To simplify, I'm using Enum, then the possible values are "INBOUND" and "OUTBOUND"
    
    **To keep simple to create one or more calls(bulk insert), the create method needs to receive a LIST of calls objects**
    """
    return CallController.create(call)

#Bulk Create
@router.post(
    "/_bulk",
    summary='Insert many CALLS'
)
async def create(calls:List[CallSchema]):
    """
    Create a call registry:

    The call object has the parameters below:
    - **caller**: simple abstraction of the caller's phone number
    - **callee**: simple abstraction of the callee's phone number
    - **started**: when the call started
    - **finished**: when the call finished
    - **duration**: will be calculated by the system, basically is a delta (duration = finished - started) => MINUTES
    - **call_type**: witch kind of call we are creating - To simplify, I'm using Enum, then the possible values are "INBOUND" and "OUTBOUND"
    
    **To keep simple to create one or more calls(bulk insert), the create method needs to receive a LIST of calls objects**
    """
    return CallController.create_many(calls)

# List
@router.get(
    "/",
    summary='List all CALLS'
)
async def list(page_number:int = 1, itens_per_page:int = 10, call_type:CallType = None):
    return CallController.list(page_number, itens_per_page, call_type)

# Get
@router.get(
    "/{call_id}",
    summary='Get a Call by ID'
)
async def get(call_id:int):
    return CallController.get(call_id)

# Delete
@router.delete(
    "/{call_id}",
    summary='Remove a CALL by ID'
)
async def remove(call_id:int):
    return CallController.remove(call_id)


# @router.get("/{item_id}")
# async def read_item(item_id: str):
#     return {"name": "Fake Specific Item", "item_id": item_id}

# @router.put(
#     "/{item_id}",
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "foo":
#         raise HTTPException(status_code=403, detail="You can only update the item: foo")
#     return {"item_id": item_id, "name": "The Fighters"}