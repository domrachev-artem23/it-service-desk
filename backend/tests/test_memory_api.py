import pytest
from app import create_app

@pytest.fixture
def client_memory():
    return create_app({"TESTING":True,"STORAGE":"memory"}).test_client()

def test_list_filters(client_memory):
    c=client_memory
    assert len(c.get('/api/tickets').json)==3
    assert len(c.get('/api/tickets?scope=open').json)==2
    assert [t['id'] for t in c.get('/api/tickets?status=new').json]==[1]
    assert len(c.get('/api/tickets?q=КОМПЬЮТЕР').json)==1
    assert c.get('/api/tickets?q=absent').json==[]

def test_crud(client_memory):
    c=client_memory
    created=c.post('/api/tickets',json={"title":"Проверка принтера","equipmentId":104})
    assert created.status_code==201
    path=created.headers['Location']
    assert c.get(path).json['status']=='new'
    assert c.patch(path,json={"status":"closed"}).json['status']=='closed'
    assert len(c.get(path+'/events').json)==2
    response=c.delete(path)
    assert response.status_code==204 and response.data==b''
    assert c.get(path).status_code==404
    assert c.delete(path).status_code==404

@pytest.mark.parametrize('data',[{},[],None,{"title":"ab","equipmentId":101},
    {"title":"Valid","equipmentId":True},{"title":"Valid","equipmentId":999},
    {"title":"Valid","equipmentId":101,"extra":1}])
def test_invalid_create(client_memory,data):
    # Explicit JSON null must be sent as data; Flask test client's json=None sends no JSON.
    if data is None:
        response=client_memory.post('/api/tickets',data='null',content_type='application/json')
    else:
        response=client_memory.post('/api/tickets',json=data)
    assert response.status_code==400
    assert 'message' in response.json['error']

def test_http_errors(client_memory):
    c=client_memory
    assert c.post('/api/tickets',data='{',content_type='application/json').status_code==400
    assert c.post('/api/tickets',data='x',content_type='text/plain').status_code==415
    assert c.patch('/api/tickets/1',json={}).status_code==400
    assert c.get('/api/tickets?status=open').status_code==400

def test_restart_resets_memory(client_memory):
    c=client_memory
    c.post('/api/tickets',json={"title":"Temporary ticket","equipmentId":101})
    assert len(c.get('/api/tickets').json)==4
    new_client=create_app({"STORAGE":"memory"}).test_client()
    assert len(new_client.get('/api/tickets').json)==3
