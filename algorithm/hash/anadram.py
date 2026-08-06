class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        sstrs = [''.join(sorted(s)) for s in strs]
        d = {}
        for i, s in enumerate(sstrs):
            if s in d:
                d[s].append(i)
            else:
                d[s] = [i]
        return [[strs[i] for i in v] for v in d.values()]


strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
solution = Solution()
print(solution.groupAnagrams(strs))