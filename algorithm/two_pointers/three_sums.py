def threeSum(nums):
    nums.sort()
    n = len(nums)
    ans = []
    print(nums)
    for i in range(n - 2):
        print(f"new {i=}", nums[i])
        if nums[i] > 0:
            print('brk')
            break
        if i and nums[i] == nums[i - 1]:
            print('cnt')
            continue
        j, k = i + 1, n - 1
        while j < k:
            print(f'{nums[i]} + {nums[j]} + {nums[k]} = {nums[i]+nums[j]+nums[k]}')
            x = nums[i] + nums[j] + nums[k]
            if x < 0:
                j += 1
            elif x > 0:
                k -= 1
            else:
                print(f'{nums[i]} + {nums[j]} + {nums[k]} = {nums[i]+nums[j]+nums[k]} hurray!')
                ans.append([nums[i], nums[j], nums[k]])
                print(f'found {i}, {j}, {k}')
                j, k = j + 1, k - 1
                while j < k and nums[j] == nums[j - 1]:
                    j += 1
                while j < k and nums[k] == nums[k + 1]:
                    k -= 1
        print('j>=k')
    return ans

nums = [-1, 0, 1, 2, -1, -4]
print(threeSum(nums))
