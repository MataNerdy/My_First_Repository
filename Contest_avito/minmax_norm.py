import sys
def read_line():
    return sys.stdin.readline().rstrip('\n')

def write(value):
    sys.stdout.write(str(value))

def writeln(value=''):
    sys.stdout.write(str(value) + '\n')

def solve():
    n, m = map(int, read_line().split())
    M = [list(map(float, read_line().split())) for _ in range(n)]
    M = [[(M[i][j] - min(M[i])) / (max(M[i]) - min(M[i])) if max(M[i]) != min(M[i]) else 0.0 for j in range(m)] for i in range(n)]

    for i in range(n):
        writeln(' '.join(f"{M[i][j]:.4f}" for j in range (m)))
solve()
