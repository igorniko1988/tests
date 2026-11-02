class RangeSum:
    def __init__(self, nums: list[int]) -> None:
        self._prefix = [0]
        for x in nums:
            self._prefix.append(self._prefix[-1] + x)

    def query(self, l: int, r: int) -> int:
        if not 0 <= l <= r < len(self._prefix) - 1:
            raise IndexError(f"bad range [{l}, {r}]")
        return self._prefix[r + 1] - self._prefix[l]
