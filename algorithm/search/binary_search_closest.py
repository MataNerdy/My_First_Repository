N, K = map(int, input().split())
a = [int(x) for x in input().split()]
b = [int(x) for x in input().split()]

for x in b:
    if x <= a[0]:
        print(a[0])
    elif x > a[N-1]:
        print(a[N-1])
    else:
        left, right  = -1, N
        while left+1 != right:
            m = (left+right) // 2
            if a[m] < x:
                left = m
            else:
                right = m
        if abs(x - a[left]) <= abs(x - a[right]):
            print(a[left])
        else:
            print(a[right])