from config import api_config
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from models import tdc_db, initialize_db
from routers import calls, index, database, statistics

### API CONFIG ###

base_api:str = api_config['base']
calls_router:str = api_config['routers']['calls']
database_router:str = api_config['routers']['database']
statistics_router:str = api_config['routers']['statistics']


### FastAPI APP ###

app = FastAPI(
    title=api_config['title'],
    description=api_config['description'],
    version=api_config['version']
)

# On startup event
@app.on_event("startup")
async def startup_event():
    # initializate database
    initialize_db()

### ROUTERS ###

# middlewares
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Open DB Connection
    tdc_db.connect(reuse_if_open=True)

    response = await call_next(request)

    # Close DB Connection
    tdc_db.close()
    
    return response

# Root
app.include_router(index.router)

# Database
app.include_router(
    database.router,
    prefix=base_api + database_router['prefix'],
    tags=database_router['tags']
)

# Calls 
app.include_router(
    calls.router,
    prefix=base_api + calls_router['prefix'],
    tags=calls_router['tags']
)

# Statistics 
app.include_router(
    statistics.router,
    prefix=base_api + statistics_router['prefix'],
    tags=statistics_router['tags']
)

