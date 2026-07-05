a = list(map(int, input().split()))
k = int(input())

first = sum(a) / 6
pair_add = 0

for prev in a:
    for cur in a:
        if cur != prev:
            pair_add += cur

pair_add /= 36

ans = first + (k - 1) * pair_add

print(ans)