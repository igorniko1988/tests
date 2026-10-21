def move_zeros(nums: list[int]) -> None:
    # write — куда поставить следующий ненулевой. O(n) время, O(1) память.
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
