def max_consecutive_chars(s):
    if not s:
        return 0
    chars = {}
    length = 0
    start = 0
    best = 0
    for i in range(len(s)):
        c = s[i]
        if c in chars and chars[c] >= start:
            start = chars[c]+1
        chars[c] = i
        length = i - start + 1
        best = max(length, best)
    return best

s = "abcabcbb"
print(max_consecutive_chars(s))