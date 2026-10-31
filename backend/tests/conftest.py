import os
from pathlib import Path
import mysql.connector
import pytest
from app import create_app

@pytest.fixture
def db_config():
    name = os.getenv("TEST_DB_NAME", "")
    if not name:
        pytest.skip("Set TEST_DB_NAME to run tests against a dedicated MySQL database")
    if not name.endswith("_test"):
        pytest.fail("TEST_DB_NAME must end in _test; refusing to reset another database")
    return {"host":os.getenv("TEST_DB_HOST", "127.0.0.1"),
            "port":int(os.getenv("TEST_DB_PORT", "3306")), "database":name,
            "user":os.getenv("TEST_DB_USER", "root"),
            "password":os.getenv("TEST_DB_PASSWORD", ""), "charset":"utf8mb4"}

@pytest.fixture
def app(db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    directory = Path(__file__).resolve().parents[2] / "database"
    for name in ("ticket_events", "tickets", "equipment"):
        cursor.execute("DROP TABLE IF EXISTS " + name)
    for file in ("schema.sql", "seed.sql"):
        source = "\n".join(line for line in (directory/file).read_text().splitlines()
                           if not line.strip().startswith("--"))
        for statement in source.split(";"):
            if statement.strip(): cursor.execute(statement)
    connection.commit(); cursor.close(); connection.close()
    return create_app({"TESTING":True, "STORAGE":"mysql", "DB_CONFIG":db_config})

@pytest.fixture
def client(app):
    return app.test_client()
