class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        sstrs = [''.join(sorted(s)) for s in strs]
        d = {}
        for i, s in enumerate(sstrs):
            if s in d:
                d[s].append(strs[i])
            else:
                d[s] = [strs[i]]
        return list(d.values())

strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
solution = Solution()
print(solution.groupAnagrams(strs))