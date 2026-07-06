import sys
def read_line():
    return sys.stdin.readline().rstrip('\n')

def write(value):
    sys.stdout.write(str(value))

def writeln(value=''):
    sys.stdout.write(str(value) + '\n')

def solve():
    line = read_line()
    ans = list(line.split())
    y = ans.count('yes')
    conv = y/len(ans)*100
    writeln(f"{conv:.2f}")

solve()
