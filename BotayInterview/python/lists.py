x = [[1]*2]*2
x[0][0] = 0
print(x)
x = [[1]*2 for _ in range(2)]
x[0][0] = 0
print(x)