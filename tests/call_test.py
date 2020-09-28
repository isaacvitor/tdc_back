from datetime import date, datetime, timedelta
from fastapi.testclient import TestClient
from main import app
import logging
import pytest
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

client = TestClient(app)

call_reference:dict = {}
calls_reference:list = []

def setup_module(module):
    # Preparing tests
    logger.info('Preparing tests - Clear all calls data')
    response = client.delete("/api/database/")
    pass

def test_001_create_a_bad_formatted_call():
    new_call = {
        'day':str(date.today()),
        'caller':123456,
        'callee':654321
    }
    response = client.post("/api/calls/", json=new_call)
    assert response.status_code == 422
    logger.info(response.json())

def test_002_create_a_good_formatted_call():
    global call_reference

    new_call = {
        'day':str(date.today()),
        'caller':123456,
        'callee':654321,
        'started':str(datetime.now()),
        'finished':str(datetime.now() + timedelta(minutes=10)),
        'call_type':'OUTBOUND'
    }
    response = client.post("/api/calls/", json=new_call)
    assert response.status_code == 200
    call_reference = response.json()
    logger.info(call_reference['id'])
    assert call_reference['id'] != 0

def test_003_remove_a_call_by_id():
    global call_reference
    logger.info(call_reference)
    # Here I'm using call_reference created in the test above
    response = client.delete('/api/calls/{}'.format(call_reference['id']))
    assert response.status_code == 200

def test_004_create_many_call():
    calls = [
        {
            'day':str(date.today()),
            'caller':123456,
            'callee':654321,
            'started':str(datetime.now()),
            'finished':str(datetime.now() + timedelta(minutes=10)),
            'call_type':'OUTBOUND'
        },
        {
            'day':str(date.today()),
            'caller':654321,
            'callee':123456,
            'started':str(datetime.now()),
            'finished':str(datetime.now() + timedelta(minutes=10)),
            'call_type':'INBOUND'
        }
    ]
    response = client.post("/api/calls/_bulk", json=calls)
    assert response.status_code == 200
    total_inserts = response.json()
    assert total_inserts >= 2

def test_005_list_calls():
    global calls_reference
    response = client.get("/api/calls/")
    assert response.status_code == 200
    calls_reference = response.json()
    assert len(calls_reference) > 0

def test_006_list_call_page_one_inbound():
    global calls_reference
    calls:list
    page_number:int = 1
    itens_per_page:int = 1
    call_type:str = 'INBOUND'
    uri:str = "/api/calls/?page_number={}&itens_per_page={}&call_type={}".format(page_number, itens_per_page, call_type)

    response = client.get(uri)
    calls = response.json()

    assert response.status_code == 200
    assert len(calls) == 1
    assert calls[0]['call_type'] == call_type

def test_007_list_call_page_one_outbound():
    global calls_reference
    calls:list
    page_number:int = 1
    itens_per_page:int = 1
    call_type:str = 'OUTBOUND'
    uri:str = "/api/calls/?page_number={}&itens_per_page={}&call_type={}".format(page_number, itens_per_page, call_type)

    response = client.get(uri)
    calls = response.json()

    assert response.status_code == 200
    assert len(calls) == 1
    assert calls[0]['call_type'] == call_type

def test_008_get_a_call_by_id():
    global calls_reference
    uri:str = "/api/calls/{}/".format(calls_reference[0]['id'])
    logger.info(uri)
    response = client.get(uri)
    call = response.json()

    assert response.status_code == 200
    assert call['id'] == calls_reference[0]['id']