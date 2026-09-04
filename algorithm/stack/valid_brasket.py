def isValid(s: str) -> bool:
    p = {
            '}': '{',
            ')': '(',
            ']': '['
        }

    stack = []

    for c in s:
        if c in p:
            print(f'{c} is in {p}')
            if not stack:
                print('not stack')
                return False
            if stack[-1] != p[c]:
                return False
            stack.pop()
        else:
            stack.append(c)
    return len(stack) == 0

s = "()"
print(isValid(s=s))