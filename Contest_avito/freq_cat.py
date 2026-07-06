import sys
def read_line():
    return sys.stdin.readline().rstrip('\n')

def write(value):
    sys.stdout.write(str(value))

def writeln(value=''):
    sys.stdout.write(str(value) + '\n')

def solve():
    line = read_line()
    cat = line.split()
    freq = {}
    best = None
    best_count = 0
    for c in cat:
        if c not in freq:
            freq[c] = 0
        freq[c] += 1
        if freq[c] > best_count:
            best_count = freq[c]
            best = c

    writeln(best)

solve()