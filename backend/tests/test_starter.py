from app import create_app

def test_health_starter():
    app = create_app({"STORAGE":"memory"})
    response = app.test_client().get('/api/health')
    assert response.status_code == 200
    assert response.json == {"status":"ok","storage":"memory"}
