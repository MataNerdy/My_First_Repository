def binary_search(list, item):
    low, high = 0, len(list) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = list[mid]
        if guess == item:
            return mid
        elif guess > item:
            high = mid - 1
        else:
            low = mid + 1

    return None
my_list = [-10, -1, 3, 5, 7, 9, 10]
print(binary_search(my_list, 3)+1)  # Output: 1
print(binary_search(my_list, -1)+1) # Output: None