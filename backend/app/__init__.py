import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from mysql.connector import Error as MySqlError
from werkzeug.exceptions import HTTPException
from .errors import ApiError
from .repository import MysqlRepository
from .routes import api
from .memory import MemoryRepository


def create_app(test_config=None):
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    app = Flask(__name__)
    app.config.update(MAX_CONTENT_LENGTH=32 * 1024)
    if test_config:
        app.config.update(test_config)
    config = app.config.get("DB_CONFIG") or {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "database": os.getenv("DB_NAME", "service_desk"),
        "user": os.getenv("DB_USER", "service_desk_app"),
        "password": os.getenv("DB_PASSWORD", ""),
        "charset": "utf8mb4",
    }
    storage = app.config.get("STORAGE") or os.getenv("STORAGE", "memory")
    if storage not in ("memory", "mysql"):
        raise ValueError("STORAGE must be memory or mysql")
    app.extensions["repository"] = (MemoryRepository() if storage == "memory"
                                    else MysqlRepository(config))
    app.register_blueprint(api, url_prefix="/api")

    @app.errorhandler(ApiError)
    def api_error(error):
        return {"error": {"code": error.code, "message": error.message}}, error.status

    @app.errorhandler(HTTPException)
    def http_error(error):
        messages = {400: "Некорректный JSON или запрос.", 404: "Ресурс не найден.",
                    405: "Метод не поддерживается.", 413: "Запрос слишком большой.",
                    415: "Используйте Content-Type: application/json."}
        return {"error": {"code": f"HTTP_{error.code}",
                          "message": messages.get(error.code, "Ошибка HTTP.")}}, error.code

    @app.errorhandler(MySqlError)
    def database_error(error):
        app.logger.exception("Database operation failed")
        return {"error": {"code": "DATABASE_UNAVAILABLE",
                          "message": "База данных временно недоступна. Повторите попытку."}}, 503

    @app.errorhandler(Exception)
    def internal_error(error):
        app.logger.exception("Unhandled application error")
        return {"error": {"code": "INTERNAL_ERROR", "message": "Ошибка сервера."}}, 500

    return app
