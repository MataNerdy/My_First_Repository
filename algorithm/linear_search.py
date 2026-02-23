N = int(input())
a = [int(x) for x in input().split()]
x = int(input())
count = 0
for i in range(N):
    if a[i] == x:
        count += 1
print(count)