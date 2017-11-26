import unittest
import os
from . import session


class SessionTest(unittest.TestCase):
    def setUp(self):
        self.username = os.environ.get("USERNAME")
        self.password = os.environ.get("PASSWORD")
        if not self.username or not self.password:
            self.fail("Must set credentials as environment variables.")

    def test_login(self):
        with session.LeetCodeSession() as s:
            self.assertFalse(s.check_login())
            self.assertTrue(s.login(self.username, self.password))
            self.assertTrue(s.check_login())
            self.assertTrue(s.logout())
            self.assertFalse(s.check_login())


if __name__ == "__main__":
    unittest.main()
