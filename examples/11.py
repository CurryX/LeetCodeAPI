class Solution:
  def maxArea(self, height):
    L, R, width, res = 0, len(height) - 1, len(height) - 1, 0
    for w in range(width, 0, -1):
        if height[L] < height[R]:
            res, L = max(res, height[L] * w), L + 1
        else:
            res, R = max(res, height[R] * w), R - 1
    return res