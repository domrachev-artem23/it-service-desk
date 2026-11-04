from contextlib import contextmanager
import mysql.connector
from .errors import ApiError

SELECT_TICKET = """
SELECT t.id, t.equipment_id AS equipmentId, t.title, t.description, t.status,
       t.created_at AS createdAt, t.updated_at AS updatedAt,
       e.name AS equipmentName, e.inventory_number AS inventoryNumber
FROM tickets t JOIN equipment e ON e.id = t.equipment_id
"""


def serialize(row):
    if row is None:
        return None
    for key in ("createdAt", "updatedAt"):
        if key in row and row[key] is not None:
            row[key] = row[key].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return row


class MysqlRepository:
    def __init__(self, config):
        self.config = config

    @contextmanager
    def transaction(self):
        connection = mysql.connector.connect(
            **self.config, 
            connection_timeout=5, 
            autocommit=False, 
            time_zone="+00:00"
        )
        cursor = connection.cursor(dictionary=True, buffered=True)
        try:
            yield cursor
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def _ticket(cursor, ticket_id):
        cursor.execute(SELECT_TICKET + " WHERE t.id = %s", (ticket_id,))
        row = cursor.fetchone()
        if row is None:
            raise ApiError("NOT_FOUND", "Заявка не найдена.", 404)
        return serialize(row)

    @staticmethod
    def _equipment(cursor, equipment_id):
        cursor.execute("SELECT id FROM equipment WHERE id = %s", (equipment_id,))
        if cursor.fetchone() is None:
            raise ApiError("EQUIPMENT_NOT_FOUND", "Оборудование не найдено.")

    @staticmethod
    def _record(cursor, ticket_id, action, message):
        cursor.execute("INSERT INTO ticket_events(ticket_id, action, message) VALUES (%s,%s,%s)",
                       (ticket_id, action, message))

    def health(self):
        with self.transaction() as cur:
            cur.execute("SELECT COUNT(*) AS count FROM tickets")
            cur.fetchone()
        return {"status": "ok", "storage": "mysql"}

    def equipment(self):
        with self.transaction() as cur:
            cur.execute("SELECT id, name, inventory_number AS inventoryNumber, location FROM equipment ORDER BY id")
            return cur.fetchall()

    def list(self, status="", scope="all", q=""):
        conditions, params = [], []
        if status:
            conditions.append("t.status = %s")
            params.append(status)
        if scope == "open":
            conditions.append("t.status <> %s")
            params.append("closed")
        if q:
            conditions.append("t.title LIKE %s ESCAPE '='")
            literal = q.replace("=", "==").replace("%", "=%").replace("-", "=")
            params.append("%" + literal + "%")
        sql = SELECT_TICKET
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY t.created_at DESC, t.id DESC"
        with self.transaction() as cur:
            cur.execute(sql, tuple(params))
            return [serialize(row) for row in cur.fetchall()]

    def get(self, ticket_id):
        with self.transaction() as cur:
            return self._ticket(cur, ticket_id)

    def create(self, values):
        with self.transaction() as cur:
            self._equipment(cur, values["equipmentId"])
            cur.execute(
                "INSERT INTO tickets(equipment_id,title,description,status) VALUES (%s,%s,%s,%s)",
                (values["equipmentId"], values["title"], values["description"], "new")
            )
            ticket_id = cur.lastrowid
            self._record(cur, ticket_id, "created", "Заявка зарегистрирована")
            return self._ticket(cur, ticket_id)

    def update(self, ticket_id, values):
        with self.transaction() as cur:
            cur.execute("SELECT id FROM tickets WHERE id=%s FOR UPDATE", (ticket_id,))
            if cur.fetchone() is None:
                raise ApiError("NOT_FOUND", "Заявка не найдена.", 404)
            old = self._ticket(cur, ticket_id)
            if "equipmentId" in values:
                self._equipment(cur, values["equipmentId"])
            columns = {"equipmentId": "equipment_id", "title": "title", "description": "description", "status": "status"}
            assignments = ", ".join(columns[key] + "=%s" for key in values)
            cur.execute(
                "UPDATE tickets SET " + assignments + ", updated_at=UTC_TIMESTAMP(6) WHERE id=%s",
                tuple(values.values()) + (ticket_id,)
            )
            message = "Обновлены поля: " + ", ".join(values)
            if "status" in values and old["status"] != values["status"]:
                labels = {"new": "Новая", "in_progress": "В работе", "closed": "Закрыта"}
                message = f"Статус: {labels[old['status']]} -> {labels[values['status']]}"
            self._record(cur, ticket_id, "updated", message)
            return self._ticket(cur, ticket_id)

    def delete(self, ticket_id):
        with self.transaction() as cur:
            cur.execute("DELETE FROM tickets WHERE id=%s", (ticket_id,))
            if cur.rowcount == 0:
                raise ApiError("NOT_FOUND", "Заявка не найдена.", 404)

    def events(self, ticket_id):
        with self.transaction() as cur:
            self._ticket(cur, ticket_id)
            cur.execute("""SELECT id, action, message, created_at AS createdAt
                           FROM ticket_events WHERE ticket_id=%s ORDER BY id DESC""", (ticket_id,))
            return [serialize(row) for row in cur.fetchall()]

    def stats(self):
        counts = {"new": 0, "in_progress": 0, "closed": 0}
        with self.transaction() as cur:
            cur.execute("SELECT status, COUNT(*) AS count FROM tickets GROUP BY status")
            for row in cur.fetchall():
                counts[row["status"]] = row["count"]
            cur.execute("SELECT COUNT(*) AS count FROM equipment")
            equipment = cur.fetchone()["count"]
        return {"total": sum(counts.values()), "byStatus": counts, "equipment": equipment}