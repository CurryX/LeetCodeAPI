count = 0


class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        print(locals())
        global count
        count += 1
        if count > 2:
            return
        hm = {}
        for i in range(0, len(nums)):
            if target - nums[i] in hm:
                return [hm[target - nums[i]], i]
            else:
                hm[nums[i]] = i


if __name__ == "__main__":
    s = Solution()
    print(s.twoSum([3, 0, 7], 10))
    print(s.twoSum([4, 0, 6], 10))
    print(s.twoSum([5, 0, 5], 10))
