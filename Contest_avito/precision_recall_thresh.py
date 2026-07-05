import sys
def read_line():
    return sys.stdin.readline().rstrip('\n')

def write(value):
    sys.stdout.write(str(value))

def writeln(value=''):
    sys.stdout.write(str(value) + '\n')

def solve():
    n = int(input())
    t = list(map(int, input().split()))
    p = list(map(float, input().split()))
    th = float(input())
    tp, tn, fp, fn = 0, 0, 0, 0
    p = [1 if x >= th else 0 for x in p]
    for i in range(n):
        if t[i] == 1 and p[i] == 1:
            tp += 1
        elif t[i] == 0 and p[i] == 0:
            tn += 1
        elif t[i] == 1 and p[i] == 0:
            fn += 1
        elif t[i] == 0 and p[i] == 1:
            fp += 1
    if tp == 0:
        p, r = 0.0, 0.0
    else:
        p = tp / (tp+fp)
        r = tp / (tp+fn)
    s = f"{p:.4f} {r:.4f}"
    writeln(s)

solve()
