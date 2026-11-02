def merge_in_place(a: list[int], m: int, b: list[int], n: int) -> None:
    i, j = m - 1, n - 1
    for pos in range(m + n - 1, -1, -1):
        if j < 0:
            break
        if i >= 0 and a[i] > b[j]:
            a[pos] = a[i]
            i -= 1
        else:
            a[pos] = b[j]
            j -= 1
