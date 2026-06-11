a = input()
i, j = 0, len(a) - 1
while i < j:
    if a[i] != a[j]:
        print("NO")
        break
    i += 1
    j -= 1
else:
    print("YES")