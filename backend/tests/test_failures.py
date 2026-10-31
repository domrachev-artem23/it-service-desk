from app import create_app
from mysql.connector import OperationalError


def test_database_failure_returns_503_without_details(monkeypatch):
    app = create_app({'TESTING': True})
    def fail():
        raise OperationalError('private database connection detail')
    monkeypatch.setattr(app.extensions['repository'], 'health', fail)
    response = app.test_client().get('/api/health')
    assert response.status_code == 503
    assert response.json['error']['code'] == 'DATABASE_UNAVAILABLE'
    assert 'private database connection' not in response.get_data(as_text=True)
