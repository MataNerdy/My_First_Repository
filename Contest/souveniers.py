n, k = map(int, input().split())
a = list(map(int, input().split()))

cnt = [0] * (k + 1)
have = 0

left = 0
cur_sum = 0
ans = 10**30

for r in range(n):
    x = a[r]
    cur_sum += x

    if x <= k:
        if cnt[x] == 0:
            have += 1
        cnt[x] += 1

    while have == k:
        ans = min(ans, cur_sum)

        y = a[left]
        cur_sum -= y

        if y <= k:
            cnt[y] -= 1
            if cnt[y] == 0:
                have -= 1

        left += 1

print(ans)