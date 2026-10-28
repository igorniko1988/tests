import copy


def build_payload(template: dict, **changes) -> dict:
    payload = copy.deepcopy(template)
    payload.update(copy.deepcopy(changes))
    return payload
