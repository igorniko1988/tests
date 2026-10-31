class RangeSum2D:
    def __init__(self, matrix: list[list[int]]) -> None:
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        self._p = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                self._p[r + 1][c + 1] = matrix[r][c] + self._p[r][c + 1] + self._p[r + 1][c] - self._p[r][c]

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        p = self._p
        return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1]
