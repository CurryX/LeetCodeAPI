from typing import List
from . import urls
from .session import LeetCodeSession
from .models import Problem


class LeetCodeClient(LeetCodeSession):
    def get_problems(self) -> List[Problem]:
        r = self.s.get(urls.PROBLEMS)
        try:
            a = r.json()["stat_status_pairs"]
            return [Problem(d) for d in a]
        except:
            return []
