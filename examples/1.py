class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        hm = {}
        for i in range(0, len(nums)):
            if target - nums[i] in hm:
                return [hm[target - nums[i]], i]
            else:
                hm[nums[i]] = i
