from .errors import ApiError

STATUSES = ("new", "in_progress", "closed")
def ticket_query(args):
    if set(args) - {"status", "scope", "q"} or any(len(args.getlist(k)) != 1 for k in args):
        raise ApiError("VALIDATION_ERROR", "Неизвестные или повторяющиеся параметры запроса.")
    status = args.get("status", "")
    scope = args.get("scope", "all")
    query = args.get("q", "").strip()
    if status and status not in STATUSES:
        raise ApiError("VALIDATION_ERROR", "Недопустимый статус фильтра.")
    if scope not in ("all", "open") or len(query) > 120:
        raise ApiError("VALIDATION_ERROR", "Некорректные параметры поиска.")
    return {"status": status, "scope": scope, "q": query}


def ticket_payload(data, partial=False):
    if not isinstance(data, dict):
        raise ApiError("VALIDATION_ERROR", "Ожидается JSON-объект.")
    allowed = {"title", "description", "equipmentId"}
    if partial:
        allowed.add("status")
    if set(data) - allowed or not data:
        raise ApiError("VALIDATION_ERROR", "Переданы неизвестные поля или пустой объект.")
    if not partial and not {"title", "equipmentId"} <= set(data):
        raise ApiError("VALIDATION_ERROR", "Укажите название и оборудование.")
    result = {}
    for key in {"title", "description"}:
        if key not in data:
            continue
        value = data[key]
        if not isinstance(value, str):
            raise ApiError("VALIDATION_ERROR", "Текстовые поля должны быть строками.")
        value = value.strip()
        minimum, maximum = (3, 120) if key == "title" else (0, 2000)
        if not minimum <= len(value) <= maximum:
            raise ApiError("VALIDATION_ERROR", f"Длина {key}: от {minimum} до {maximum} символов.")
        result[key] = value
    if "equipmentId" in data:
        value = data["equipmentId"]
        if type(value) is not int or value < 1:
            raise ApiError("VALIDATION_ERROR", "Выберите оборудование из списка.")
        result["equipmentId"] = value
    if "status" in data:
        if data["status"] not in STATUSES:
            raise ApiError("VALIDATION_ERROR", "Недопустимый статус заявки.")
        result["status"] = data["status"]
    if not partial:
        result.setdefault("description", "")
        result["status"] = "new"
    return result