from .errors import ApiError

STATUSES = ("new", "in_progress", "closed")


def ticket_payload(data, partial=False):
    # TODO(LR2): реализуйте ticket_payload по методичке.
    raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)


def ticket_query(args):
    # TODO(LR2): реализуйте ticket_query по методичке.
    raise ApiError("NOT_IMPLEMENTED", "Этот шаг лабораторной работы ещё не выполнен.", 501)
