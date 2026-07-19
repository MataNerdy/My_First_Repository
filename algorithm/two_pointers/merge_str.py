def mergeAlternately(word1, word2):
    res = ''
    i, j = 0, 0
    n, k = len(word1), len(word2)
    while i<n or j<k:
        if i<n:
            res += word1[i]
            i += 1
        if j<k:
            res += word2[j]
            j += 1
    return res

print(mergeAlternately("abc", "prq"))