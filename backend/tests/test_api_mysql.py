import pytest
from app import create_app

pytestmark = pytest.mark.integration
PAYLOAD = {"title":"Тестовая неисправность", "equipmentId":101, "description":"Проверка"}

def test_crud_and_persistence(client, app, db_config):
    response = client.post('/api/tickets', json=PAYLOAD)
    assert response.status_code == 201
    ticket_id = response.json['id']
    assert response.headers['Location'] == f'/api/tickets/{ticket_id}'
    another_client = create_app({"STORAGE":"mysql", "DB_CONFIG":db_config}).test_client()
    assert another_client.get(f'/api/tickets/{ticket_id}').json['title'] == PAYLOAD['title']
    result = client.patch(f'/api/tickets/{ticket_id}', json={"status":"closed"})
    assert result.status_code == 200 and result.json['status'] == 'closed'
    history = client.get(f'/api/tickets/{ticket_id}/events').json
    assert [item['action'] for item in history] == ['updated','created']
    deleted = client.delete(f'/api/tickets/{ticket_id}')
    assert deleted.status_code == 204 and not deleted.data
    assert client.get(f'/api/tickets/{ticket_id}').status_code == 404
    with app.extensions['repository'].transaction() as cur:
        cur.execute('SELECT COUNT(*) AS count FROM ticket_events WHERE ticket_id=%s', (ticket_id,))
        assert cur.fetchone()['count'] == 0

def test_join_and_stats(client):
    tickets = client.get('/api/tickets').json
    assert len(tickets) == 3 and tickets[0]['equipmentName']
    stats = client.get('/api/stats').json
    assert stats == {'total':3,'equipment':4,'byStatus':{'new':1,'in_progress':1,'closed':1}}
    assert client.get('/api/health').json['storage'] == 'mysql'
    assert len(client.get('/api/equipment').json) == 4

def test_search_and_filters(client):
    assert len(client.get('/api/tickets?scope=open').json) == 2
    result = client.get('/api/tickets', query_string={'q':'  КОМПЬЮТЕР  ','status':'new'}).json
    assert [item['id'] for item in result] == [1]
    assert client.get('/api/tickets?q=definitely-absent').json == []
    assert client.get('/api/tickets?status=open').status_code == 400

def test_search_literals_and_sql_injection(client):
    title = "Принтер 100%_готов = yes ' OR 1=1 --"
    client.post('/api/tickets', json={**PAYLOAD,'title':title})
    result = client.get('/api/tickets', query_string={'q':'%_'}).json
    assert len(result) == 1 and result[0]['title'] == title
    assert client.get('/api/tickets', query_string={'q':"x' OR 1=1 --"}).json == []
    assert client.get('/api/stats').json['total'] == 4

@pytest.mark.parametrize('path,method,payload,status', [
    ('/api/tickets','post',{'title':'ab','equipmentId':101},400),
    ('/api/tickets','post',{**PAYLOAD,'equipmentId':999},400),
    ('/api/tickets/999','patch',{'status':'new'},404),
    ('/api/tickets/999','delete',None,404),
    ('/api/tickets/1','patch',{},400),
    ('/api/tickets/1','patch',{'equipmentId':999},400),
])
def test_api_errors(client,path,method,payload,status):
    response = getattr(client,method)(path, json=payload)
    assert response.status_code == status and 'message' in response.json['error']

def test_http_errors(client):
    assert client.post('/api/tickets', data='broken', content_type='text/plain').status_code == 415
    assert client.post('/api/tickets', data='{', content_type='application/json').status_code == 400
    assert client.put('/api/tickets/1', json={}).status_code == 405
    assert client.get('/api/not-found').status_code == 404
    assert client.post('/api/tickets', data='x'*40000,content_type='application/json').status_code == 413

def test_transaction_rollback_when_event_fails(app, client, monkeypatch):
    repository = app.extensions['repository']
    before = client.get('/api/stats').json['total']
    def fail(*args): raise RuntimeError('internal implementation detail')
    monkeypatch.setattr(repository, '_record', fail)
    response = client.post('/api/tickets', json=PAYLOAD)
    assert response.status_code == 500
    assert 'implementation detail' not in response.get_data(as_text=True)
    assert client.get('/api/stats').json['total'] == before
    old = client.get('/api/tickets/1').json
    assert client.patch('/api/tickets/1', json={'status':'closed'}).status_code == 500
    assert client.get('/api/tickets/1').json == old
