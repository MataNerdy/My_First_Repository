def lengthOfLongestSubstring(s: str) -> int:
    ch = {}
    max_len = 0
    l = 0

    for r, c in enumerate(s):
        if c in ch and ch[c] >= l:
            l = ch[c] + 1
        ch[c] = r
        max_len = max(max_len, r-l +1)
    return max_len