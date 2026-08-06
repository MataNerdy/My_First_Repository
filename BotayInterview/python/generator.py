data = [x**2 for x in range(10)]
result = [x for x in data if x%2 == 0]
print(data)
print(result)

data = (x**2 for x in range(10))
result = (x for x in range(20) if x%2 == 0)
for d in data:
    print(f"Data: {d}")
    print(f"Result: {next(result)}")

def countdown(n):
    while n > 0:
        yield n
        n -= 1

for k in countdown(5):
    print(k)