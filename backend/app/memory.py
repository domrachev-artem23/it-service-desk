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
        # TODO(LR2): реализуйте list по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

    def get(self, ticket_id):
        # TODO(LR2): реализуйте get по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

    def create(self, values):
        # TODO(LR2): реализуйте create по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

    def update(self, ticket_id, values):
        # TODO(LR2): реализуйте update по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

    def delete(self, ticket_id):
        # TODO(LR2): реализуйте delete по методичке.
        raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)

    def events(self, ticket_id):
        self._item(ticket_id)
        return deepcopy([event for event in reversed(self.history) if event["ticketId"] == ticket_id])

    def stats(self):
        counts = {status:sum(item["status"]==status for item in self.items)
                  for status in ("new","in_progress","closed")}
        return {"total":len(self.items),"equipment":len(self.devices),"byStatus":counts}
