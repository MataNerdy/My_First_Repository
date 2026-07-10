def lengthOfLIS(nums):
    tails = []
    for n in nums:
        print(tails)
        l, r = 0, len(tails)
        while l<r:
            m = (l+r) // 2
            if tails[m] < n:
                l = m + 1
            else:
                r = m
        if l == len(tails):
            tails.append(n)
        else:
            tails[l] = n
    return len(tails)

lengthOfLIS([10, 5, 8, 3, 9, 4, 12, 11])