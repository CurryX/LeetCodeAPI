import unittest
import os
from . import session, apis


class LeetCodeTestCase(unittest.TestCase):
    username = ""
    password = ""

    @classmethod
    def setUpClass(cls):
        cls.username = os.environ.get("USERNAME")
        cls.password = os.environ.get("PASSWORD")
        if not cls.username or not cls.password:
            raise Exception("Must set credentials as environment variables.")


class SessionTest(LeetCodeTestCase):
    def test_login(self):
        with session.LeetCodeSession() as s:
            self.assertFalse(s.check_login())
            self.assertTrue(s.login(self.username, self.password))
            self.assertTrue(s.check_login())
            self.assertTrue(s.logout())
            self.assertFalse(s.check_login())


class ClientTest(LeetCodeTestCase):
    c = apis.LeetCodeClient()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.c.login(cls.username, cls.password)

    def test_get_problems(self):
        problems = self.c.get_problems()
        self.assertIsNotNone(problems)
        self.assertGreater(len(problems), 100)
        results = [p for p in problems if p.id == 1]
        self.assertEqual(len(results), 1)
        two_sum = results[0]
        self.assertEqual(two_sum.title_slug, "two-sum")
        self.assertEqual(two_sum.title, "Two Sum")
        self.assertEqual(two_sum.level, 1)
        self.assertGreater(two_sum.total_acs, 0)
        self.assertGreater(two_sum.total_submitted, 0)

    def test_submission(self):
        id = self.c.submit("python", 1, "two-sum", """
class Solution:
    def twoSum(self, nums, target):
        hm = {}
        for i in range(0, len(nums)):
            if target-nums[i] in hm:
                return [hm[target-nums[i]], i]
            else:
                hm[nums[i]]=i
        """)
        self.assertGreater(id, 0)
        for i in range(5):
            submission = self.c.submission_status(id)
            if submission.state == "SUCCESS":
                break
        else:
            self.fail()
        self.assertEqual(submission.status_msg, "Accepted")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.c.close()


if __name__ == "__main__":
    unittest.main()
