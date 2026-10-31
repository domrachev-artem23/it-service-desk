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
        # TODO(LR3): реализуйте transaction по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

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
        # TODO(LR3): реализуйте list по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

    def get(self, ticket_id):
        with self.transaction() as cur:
            return self._ticket(cur, ticket_id)

    def create(self, values):
        # TODO(LR3): реализуйте create по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

    def update(self, ticket_id, values):
        # TODO(LR3): реализуйте update по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

    def delete(self, ticket_id):
        # TODO(LR3): реализуйте delete по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

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
