def req_sum(arr):
    if len(arr) == 0:
        return 0
    else:
        return arr[0] + req_sum(arr[1:])

print(req_sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

def req_count(arr):
    if len(arr) == 0:
        return 0
    else:
        return 1 + req_count(arr[1:])

print(req_count([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

def req_max(arr):
    if len(arr) == 1:
        return arr[0]
    elif len(arr) == 2:
        return arr[0] if arr[0] > arr[1] else arr[1]
    else:
        max_rest = req_max(arr[1:])
        return arr[0] if arr[0] > max_rest else max_rest

print(req_max([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))