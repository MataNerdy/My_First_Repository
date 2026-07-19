def removeDuplicates(nums):
    i = 0
    for x in nums:
        if i == 0 or x != nums[i-1]:
            nums[i] = x
            i += 1
    return i