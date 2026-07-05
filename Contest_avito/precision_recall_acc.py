import sys
def read_line():
    return sys.stdin.readline().rstrip('\n')

def write(value):
    sys.stdout.write(str(value))

def writeln(value=''):
    sys.stdout.write(str(value) + '\n')

def solve():
    line = read_line().strip()
    tp, fp, tn, fn = map(int, line.split())
    if tp == 0:
        res = [0.0 for _ in range(3)]
    else:
        p = tp / (tp+fp)
        r = tp / (tp+fn)
        acc = (tp+tn) / (tp+fp+tn+fn)
        res = [acc, p, r]
    s = ' '.join(f"{x:.4f}" for x in res)
    writeln(s)

solve()
