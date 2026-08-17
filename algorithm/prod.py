def productExceptSelf(nums):
    n = len(nums)
    res1 = [1]*len(nums)
    res2 = [1]*len(nums)
    for i in range(1, n-1):
        res1[i] *= nums[i-1]
        res1[i+1] = res1[i]
    res1[i+1] *= nums[i]
    for i in range(n-1, 1, -1):
        res2[i-1] *= nums[i]
        res2[i-2] = res2[i-1]
    res2[i-2] *= nums[i-1]
    res = [x*y for x, y in zip(res1, res2)]
    return res

nums = [1, 2, 3, 4, 5, 6]
print(productExceptSelf(nums=nums))