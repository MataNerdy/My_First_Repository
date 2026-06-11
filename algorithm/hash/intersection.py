def intersect(nums1, nums2):
    count = {}
    for n in nums1:
        if n in count:
            count[n] += 1
        else:
            count[n] = 1
    result = []

    for n in nums2:
        if n in count:
            result.append(n)
    return result
