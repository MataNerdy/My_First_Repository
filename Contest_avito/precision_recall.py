import sys
def read_line():
    return sys.stdin.readline().rstrip('\n')

def write(value):
    sys.stdout.write(str(value))

def writeln(value=''):
    sys.stdout.write(str(value) + '\n')

def solve():
    line = read_line().strip()
    tp, fp, fn = map(int, line.split())
    ap = tp+fp
    at = tp+fn
    if tp == 0:
        p = 0
        r = 0
    else:
        p = tp/ap
        r = tp/at
    s = f"{p:.4f} {r:.4f}"
    writeln(s)

solve()
