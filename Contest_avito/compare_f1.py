import sys
def read_line():
    return sys.stdin.readline().rstrip('\n')

def write(value):
    sys.stdout.write(str(value))

def writeln(value=''):
    sys.stdout.write(str(value) + '\n')

def f1(tp, fp, fn):
    if tp == 0:
        return 0.0
    else:
        p = tp / (tp+fp)
        r = tp / (tp+fn)
        f1 = 2 / (1/p + 1/r)
        return f1

def solve():
    n = int(input())
    b = -1
    idx = -1
    for i in range(n):
        tp, fp, fn = map(int, input().split())
        f = f1(tp, fp, fn)
        if f > b:
            b = f
            idx = i
    writeln(idx+1)

solve()
