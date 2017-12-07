import io
import sys
import unittest

from ..leetcode.tests import LeetCodeTestCase
from ..leetcode import apis
from .injection import inject, find_funcs


class InjectionTest(unittest.TestCase):
    def test_injection(self):
        src = inject("""
class Solution:
    def twoSum(self, nums, target):
        hm = {}
        for i in range(0, len(nums)):
            if target-nums[i] in hm:
                return [hm[target-nums[i]], i]
            else:
                hm[nums[i]]=i
        """, ["twoSum"], 2)
        src += """
s = Solution()
print(s.twoSum([1234, 0, 4321], 5555))
print(s.twoSum([2345, 0, 5432], 9999))
        """
        stdout = sys.stdout
        sys.stdout = io.StringIO()
        exec(compile(src, "two_sum", "exec"))
        output: str = sys.stdout.getvalue()
        sys.stdout = stdout
        lines = output.splitlines()
        self.assertGreaterEqual(len(lines), 4)
        self.assertIn("5555", lines[0])
        self.assertIn("1234", lines[0])
        self.assertIn("4321", lines[0])
        self.assertEqual(lines[1], str([0, 2]))
        self.assertIn("9999", lines[2])
        self.assertIn("2345", lines[2])
        self.assertIn("5432", lines[2])
        self.assertEqual(lines[3], str(None))

    def test_find_funcs(self):
        funcs = find_funcs("""
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        pass
    def __second2Function__(self):
        pass
""")
        self.assertEqual(len(funcs), 2)
        self.assertIn("addTwoNumbers", funcs)
        self.assertIn("__second2Function__", funcs)


class DataCrawlerTest(LeetCodeTestCase):
    c = apis.LeetCodeClient()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.c.login(cls.username, cls.password)


if __name__ == "__main__":
    unittest.main()
