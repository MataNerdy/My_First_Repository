def maxArea(height):
    left = 0
    right = len(height) - 1
    max_water = 0
    while left < right:
        w = right - left
        h = min(height[left], height[right])
        cur = w * h
        max_water = max(max_water, cur)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water
