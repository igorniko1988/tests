"""t03 (разминка, 10 мин). Move Zeroes — LeetCode 283.

Перенеси все нули в конец, сохранив порядок остальных элементов.
Менять список НА МЕСТЕ, дополнительная память O(1), вернуть None.
Нельзя создавать новый список (и nums[:] = ... тоже не считается).

nums = [0, 1, 0, 3, 12]; move_zeros(nums); nums -> [1, 3, 12, 0, 0]

Подсказка, если застрял: указатель «куда ставить следующий ненулевой».
"""


def move_zeros(nums: list[int]) -> None:
    write = 0
    for num in range(len(nums)):
        if nums[num] != 0:
            nums[write], nums[num] = nums[num], nums[write]
            write +=1
    return None


print(move_zeros([0, 1, 0, 3, 12]))
