def json_diff(old: dict, new: dict) -> dict[str, list[str]]:
    old_keys, new_keys = old.keys(), new.keys()
    return {
        "added": sorted(new_keys - old_keys),
        "removed": sorted(old_keys - new_keys),
        "changed": sorted(k for k in old_keys & new_keys if old[k] != new[k]),
    }
