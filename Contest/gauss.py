def features(x):
    res = [1.0]

    for i in range(5):
        res.append(x[i])

    for i in range(5):
        for j in range(i, 5):
            res.append(x[i] * x[j])

    return res


def solve_gauss(A, b):
    n = len(A)

    for col in range(n):
        pivot = col

        for row in range(col + 1, n):
            if abs(A[row][col]) > abs(A[pivot][col]):
                pivot = row

        A[col], A[pivot] = A[pivot], A[col]
        b[col], b[pivot] = b[pivot], b[col]

        div = A[col][col]

        for j in range(col, n):
            A[col][j] /= div
        b[col] /= div

        for row in range(n):
            if row == col:
                continue

            factor = A[row][col]

            for j in range(col, n):
                A[row][j] -= factor * A[col][j]

            b[row] -= factor * b[col]

    return b


D = 21

X = []
y = []

for _ in range(1000):
    nums = list(map(float, input().split()))
    x = nums[:5]
    value = nums[5]

    X.append(features(x))
    y.append(value)

A = [[0.0] * D for _ in range(D)]
b = [0.0] * D

for row, value in zip(X, y):
    for i in range(D):
        b[i] += row[i] * value

        for j in range(D):
            A[i][j] += row[i] * row[j]

coef = solve_gauss(A, b)


for _ in range(1000):
    nums = list(map(float, input().split()))
    row = features(nums)

    ans = 0.0
    for i in range(D):
        ans += coef[i] * row[i]

    print(f"{ans:.10f}")