"""Initialize a NEW local MySQL database, preserving existing databases.
Run from the repository root with the backend virtual environment.
"""
import argparse
import getpass
import re
from pathlib import Path
import mysql.connector

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=3306)
parser.add_argument("--admin", default="root")
parser.add_argument("--database", default="service_desk")
parser.add_argument("--app-user", default="service_desk_app")
args = parser.parse_args()
for value in (args.database, args.app_user):
    if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_]{0,40}", value):
        parser.error("Use 1–41 Latin letters, digits and underscores, starting with a letter")
admin_password = getpass.getpass("MySQL administrator password: ")
app_password = getpass.getpass("New application user password (at least 12 characters): ")
if len(app_password) < 12:
    parser.error("Application password must contain at least 12 characters")
connection = mysql.connector.connect(host=args.host, port=args.port, user=args.admin,
                                     password=admin_password, charset="utf8mb4")
cur = connection.cursor()
try:
    cur.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME=%s", (args.database,))
    if cur.fetchone():
        raise SystemExit("Database already exists; refusing to overwrite it. Select a NEW database name.")
    cur.execute("SELECT User FROM mysql.user WHERE User=%s", (args.app_user,))
    if cur.fetchone():
        raise SystemExit("User already exists; select a NEW app-user name.")
    cur.execute(f"CREATE DATABASE `{args.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci")
    cur.execute(f"USE `{args.database}`")
    for file in ("schema.sql", "seed.sql"):
        content = "\n".join(line for line in Path(__file__).with_name(file).read_text().splitlines()
                            if not line.strip().startswith("--"))
        for sql in content.split(";"):
            if sql.strip(): cur.execute(sql)
    connection.commit()
    cur.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s", (args.app_user, app_password))
    cur.execute(f"GRANT SELECT,INSERT,UPDATE,DELETE ON `{args.database}`.* TO %s@'localhost'", (args.app_user,))
    print("Created database and local application user. Set backend/.env to these values.")
finally:
    cur.close()
    connection.close()
