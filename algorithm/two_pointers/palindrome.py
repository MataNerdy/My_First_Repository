def isPalindrome(s: str):
    s = s.lower()
    s = ''.join(c for c in s if c.isalnum())
    i, j = 0, len(s)-1
    while i <= j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True

s = "0P"
print(isPalindrome(s))