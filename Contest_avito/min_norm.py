import sys
def read_line():
    return sys.stdin.readline().rstrip('\n')

def write(value):
    sys.stdout.write(str(value))

def writeln(value=''):
    sys.stdout.write(str(value) + '\n')

def solve():
    xs = list(map(int, input().split()))
    mn = min(xs)
    mx = max(xs)
    d = mx - mn
    if d == 0:
        res = [0.0 for x in xs]
    else:
        res = [(x-mn)/d for x in xs]
    s = ' '.join(f"{x:.4f}" for x in res)
    writeln(s)

solve()
