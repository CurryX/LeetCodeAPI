class Solution:
    def isPalindrome(self, x):
        if x < 0:
            return False

        r = 1
        while x / r >= 10:
            r *= 10

        while r > 1:
            left, x =divmod(x, r)
            x, right = divmod(x, 10)
            if left != right:
                return False
            r //= 100

        return True