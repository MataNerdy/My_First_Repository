for _ in range(100):
    nums = list(map(float, input().split()))

    s = 0.0

    for i in range(0, 2000, 2):
        x = nums[i]
        y = nums[i + 1]

        s += x * x + y * y

    mean_r2 = s / 1000

    if mean_r2 < 5.0 / 12.0:
        print(1)
    else:
        print(2)