def merge(intervals):
    intervals.sort()
    cur = [intervals[0]]
    for b, e in intervals:
        if b <= cur[-1][1]:
            cur[-1][1] = max(e, cur[-1][1])
        else:
            cur.append([b, e])
    return cur