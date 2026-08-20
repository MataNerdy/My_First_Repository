def isPalindrome(s: str):
    s = list(s.lower())
    s1 = ''
    for x in s:
        if x.isalpha():
            print(x)
            s1 += x
    return s1 == s1[::-1]


s = "A man, a plan, a canal: Panama"
print(isPalindrome(s))