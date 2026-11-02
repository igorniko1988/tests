from collections import Counter


def compare_responses(expected: list[dict], actual: list[dict]) -> dict[str, list[int]]:
    expected_by_id = {record["id"]: record for record in expected}
    actual_by_id = {}
    for record in actual:
        actual_by_id.setdefault(record["id"], record)  # первая запись с этим id
    counts = Counter(record["id"] for record in actual)
    return {
        "missing": sorted(expected_by_id.keys() - actual_by_id.keys()),
        "extra": sorted(actual_by_id.keys() - expected_by_id.keys()),
        "mismatched": sorted(
            i for i in expected_by_id.keys() & actual_by_id.keys() if expected_by_id[i] != actual_by_id[i]
        ),
        "duplicated": sorted(i for i, n in counts.items() if n > 1),
    }
