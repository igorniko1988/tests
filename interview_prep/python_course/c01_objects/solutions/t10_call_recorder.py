import copy


class CallRecorder:
    def __init__(self):
        self._calls = []

    def __call__(self, *args, **kwargs):
        self._calls.append(copy.deepcopy((args, kwargs)))

    @property
    def calls(self) -> list[tuple[tuple, dict]]:
        return copy.deepcopy(self._calls)

    @property
    def last(self):
        return copy.deepcopy(self._calls[-1]) if self._calls else None

    @property
    def count(self) -> int:
        return len(self._calls)
