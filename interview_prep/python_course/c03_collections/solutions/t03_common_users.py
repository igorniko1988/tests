def common_users(first: list[dict], second: list[dict]) -> list[int]:
    in_second = {u["id"] for u in second}
    result, seen = [], set()
    for user in first:
        uid = user["id"]
        if uid in in_second and uid not in seen:
            seen.add(uid)
            result.append(uid)
    return result
