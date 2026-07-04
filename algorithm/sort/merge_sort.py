def merge(left, right):
    print(f'Merging {left} and {right}')
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        print(i, j)
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        print(result)
    result.extend(left[i:])
    result.extend(right[j:])
    print(f'Merged into {result}')
    return result


def merge_sort(arr):
    if len(arr) < 2:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

print(merge_sort([38, 27, 43, 3, 9, 82, 10, 1]))