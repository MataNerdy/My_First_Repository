def sortedSquares(nums):
    n = len(nums)
    result = [0]*n
    i, j, idx = 0, n-1, n-1
    while i <= j:
        if abs(nums[i]) <= abs(nums[j]):
            result[idx] = nums[j]**2
            j -= 1
        else:
            result[idx] = nums[i]**2
            i += 1
        idx -= 1
    return result