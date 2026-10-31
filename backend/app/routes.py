from flask import Blueprint, current_app, request, url_for
from .errors import ApiError
from .validation import ticket_payload, ticket_query

api = Blueprint("api", __name__)


def repo():
    return current_app.extensions["repository"]


@api.get("/health")
def health():
    return repo().health()


@api.get("/equipment")
def equipment():
    return repo().equipment()


@api.get("/stats")
def stats():
    return repo().stats()


@api.get("/tickets")
def tickets():
    # TODO(LR2): реализуйте tickets по методичке.
    raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)


@api.get("/tickets/<int:ticket_id>")
def ticket(ticket_id):
    # TODO(LR2): реализуйте ticket по методичке.
    raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)


@api.post("/tickets")
def create_ticket():
    # TODO(LR2): реализуйте create_ticket по методичке.
    raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)


@api.patch("/tickets/<int:ticket_id>")
def update_ticket(ticket_id):
    # TODO(LR2): реализуйте update_ticket по методичке.
    raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)


@api.delete("/tickets/<int:ticket_id>")
def delete_ticket(ticket_id):
    # TODO(LR2): реализуйте delete_ticket по методичке.
    raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)


@api.get("/tickets/<int:ticket_id>/events")
def ticket_events(ticket_id):
    return repo().events(ticket_id)
