def move_zeros(nums: list[int]) -> None:
    write = 0  # сюда кладём следующий ненулевой
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
