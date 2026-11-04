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
    return repo().list(**ticket_query(request.args))


@api.get("/tickets/<int:ticket_id>")
def ticket(ticket_id):
    return repo().get(ticket_id)


@api.post("/tickets")
def create_ticket():
    result = repo().create(ticket_payload(request.get_json()))
    return result, 201, {"Location": url_for("api.ticket", ticket_id=result["id"])}


@api.patch("/tickets/<int:ticket_id>")
def update_ticket(ticket_id):
    return repo().update(ticket_id, ticket_payload(request.get_json(), partial=True))


@api.delete("/tickets/<int:ticket_id>")
def delete_ticket(ticket_id):
    repo().delete(ticket_id)
    return "", 204


@api.get("/tickets/<int:ticket_id>/events")
def ticket_events(ticket_id):
    return repo().events(ticket_id)