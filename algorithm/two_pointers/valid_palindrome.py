def validPalindrome(s: str) -> bool:
    def isPalindrom(i:int, j:int) -> bool:
        while i<j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    lft, rgt = 0, len(s)-1
    while lft<rgt:
        if s[lft]!=s[rgt]:
            return isPalindrom(lft+1, rgt) or isPalindrom(lft, rgt-1)
        lft += 1
        rgt -= 1
    return True