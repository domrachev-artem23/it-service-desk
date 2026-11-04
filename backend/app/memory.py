from copy import deepcopy
from datetime import datetime, timezone
from .errors import ApiError


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


class MemoryRepository:
    def __init__(self):
        self.devices = [
            {"id":101,"name":"Рабочая станция Lenovo ThinkCentre","inventoryNumber":"PC-0204-01","location":"Аудитория 204"},
            {"id":102,"name":"Проектор Epson EB-X49","inventoryNumber":"PR-0301-01","location":"Аудитория 301"},
            {"id":103,"name":"Коммутатор TP-Link TL-SG1024","inventoryNumber":"NET-0101-01","location":"Серверная"},
            {"id":104,"name":"Принтер HP LaserJet Pro","inventoryNumber":"PRN-0200-01","location":"Кабинет ИТ-отдела"},
        ]
        self.items = []
        self.history = []
        self.next_id = 1
        for equipment_id, title, status in [
            (101,"Не включается компьютер в аудитории 204","new"),
            (102,"Проектор не выводит изображение","in_progress"),
            (103,"Восстановить подключение к локальной сети","closed"),
        ]:
            timestamp = now()
            self.items.append({"id":self.next_id,"equipmentId":equipment_id,"title":title,
                               "description":"Учебное обращение","status":status,
                               "createdAt":timestamp,"updatedAt":timestamp})
            self._record(self.next_id,"created","Учебная заявка загружена")
            self.next_id += 1

    def health(self):
        return {"status":"ok","storage":"memory"}

    def equipment(self):
        return deepcopy(self.devices)

    def _device(self, equipment_id):
        for device in self.devices:
            if device["id"] == equipment_id:
                return device
        raise ApiError("EQUIPMENT_NOT_FOUND","Оборудование не найдено.")

    def _item(self, ticket_id):
        for item in self.items:
            if item["id"] == ticket_id:
                return item
        raise ApiError("NOT_FOUND","Заявка не найдена.",404)

    def _decorate(self, item):
        device = self._device(item["equipmentId"])
        return {**deepcopy(item),"equipmentName":device["name"],
                "inventoryNumber":device["inventoryNumber"]}

    def _record(self, ticket_id, action, message):
        self.history.append({"id":len(self.history)+1,"ticketId":ticket_id,
                             "action":action,"message":message,"createdAt":now()})

    def list(self, status="", scope="all", q=""):
        result = self.items
        if status:
            result = [item for item in result if item["status"] == status]
        if scope == "open":
            result = [item for item in result if item["status"] != "closed"]
        if q:
            result = [item for item in result if q.casefold() in item["title"].casefold()]
        return [self._decorate(item) for item in reversed(result)]

    def get(self, ticket_id):
        return self._decorate(self._item(ticket_id))

    def create(self, values):
        self._device(values["equipmentId"])
        timestamp = now()
        item = {**values, "id": self.next_id, "status": "new",
                "createdAt": timestamp, "updatedAt": timestamp}
        self.next_id += 1
        self.items.append(item)
        self._record(item["id"], "created", "Заявка зарегистрирована")
        return self._decorate(item)

    def update(self, ticket_id, values):
        item = self._item(ticket_id)
        if "equipmentId" in values:
            self._device(values["equipmentId"])
        item.update(values)
        item["updatedAt"] = now()
        self._record(ticket_id, "updated", "Обновлена заявка")
        return self._decorate(item)

    def delete(self, ticket_id):
        item = self._item(ticket_id)
        self.items.remove(item)
        self.history = [event for event in self.history if event["ticketId"] != ticket_id]

    def events(self, ticket_id):
        self._item(ticket_id)
        return deepcopy([event for event in reversed(self.history) if event["ticketId"] == ticket_id])

    def stats(self):
        counts = {status:sum(item["status"]==status for item in self.items)
                  for status in ("new","in_progress","closed")}
        return {"total":len(self.items),"equipment":len(self.devices),"byStatus":counts}