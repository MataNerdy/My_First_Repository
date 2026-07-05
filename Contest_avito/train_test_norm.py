import sys


def read_line():
    return sys.stdin.readline().rstrip("\n")


def writeln(value=""):
    sys.stdout.write(str(value) + "\n")


def solve():
    train = list(map(float, read_line().split()))
    test = list(map(float, read_line().split()))

    mn = min(train)
    mx = max(train)
    d = mx - mn

    if d == 0:
        tr_res = [0.0 for _ in train]
        ts_res = [0.0 for _ in test]
    else:
        tr_res = [(x - mn) / d for x in train]
        ts_res = [(x - mn) / d for x in test]

    s1 = " ".join(f"{x:.4f}" for x in tr_res)
    s2 = " ".join(f"{x:.4f}" for x in ts_res)

    writeln(s1)
    writeln(s2)

solve()