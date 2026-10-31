import pytest
from app.validation import ticket_payload, ticket_query
from app.errors import ApiError
from werkzeug.datastructures import MultiDict

@pytest.mark.parametrize("data", [None, [], {}, {"title":"ok", "equipmentId":101},
    {"title":"   ", "equipmentId":101}, {"title":"valid", "equipmentId":True},
    {"title":"valid", "equipmentId":1.5}, {"title":"valid", "equipmentId":0},
    {"title":"valid", "equipmentId":101, "status":"closed"},
    {"title":"valid", "equipmentId":101, "description":3}])
def test_invalid_create(data):
    with pytest.raises(ApiError): ticket_payload(data)

def test_normalization():
    assert ticket_payload({"title":"  Printer  ", "equipmentId":101}) == {
        "title":"Printer", "equipmentId":101, "description":"", "status":"new"}

@pytest.mark.parametrize("data", [{}, {"id":1}, {"status":"open"}, {"description":"x"*2001}])
def test_invalid_patch(data):
    with pytest.raises(ApiError): ticket_payload(data, partial=True)

@pytest.mark.parametrize("pairs", [[('status','open')],[('scope','bad')],[('q','a'),('q','b')],[('unknown','x')]])
def test_invalid_filters(pairs):
    with pytest.raises(ApiError): ticket_query(MultiDict(pairs))
