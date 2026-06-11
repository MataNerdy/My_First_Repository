def moveZeroes(nums: list) -> list:
    i = 0
    for j in range(len(nums)):
        print(i, j, nums)
        if nums[j] != 0:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    return nums

print(moveZeroes([3, 0, 1, 0, 3, 12]))