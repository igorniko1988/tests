def deepcopy_cycles(obj, memo: dict | None = None):
    if memo is None:
        memo = {}
    if id(obj) in memo:
        return memo[id(obj)]
    if isinstance(obj, list):
        copy_ = []
        memo[id(obj)] = copy_          # запомнить ДО обхода детей — иначе цикл бесконечен
        copy_.extend(deepcopy_cycles(item, memo) for item in obj)
        return copy_
    if isinstance(obj, dict):
        copy_ = {}
        memo[id(obj)] = copy_
        for key, value in obj.items():
            copy_[key] = deepcopy_cycles(value, memo)
        return copy_
    return obj
