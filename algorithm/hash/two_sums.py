def twoSum(nums: list[int], target: int) -> list[int]:
    s = {}
    for i, num in enumerate(nums):
        rest = target-num
        if rest in s:
            return [s[rest], i]
        else:
            s[num] = i
    return []

print(twoSum([2, 7, 11, 15], 9))