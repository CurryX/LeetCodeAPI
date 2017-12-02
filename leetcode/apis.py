from typing import List
from . import urls
from .session import LeetCodeSession
from .models import Problem, Submission


class LeetCodeClient(LeetCodeSession):
    def get_problems(self) -> List[Problem]:
        r = self.s.get(urls.PROBLEMS)
        try:
            a = r.json()["stat_status_pairs"]
            return [Problem(d) for d in a]
        except:
            return []

    def submit(self, lang: str, question_id: int, question_slug: str, code: str) -> int:
        csrf = self.s.cookies.get("csrftoken")
        r = self.s.post(urls.SUBMIT % question_slug,
                        json={"lang": lang, "question_id": question_id, "typed_code": code},
                        headers={"referer": urls.DESCRIPTION % question_slug,
                                 "X-CSRFToken": csrf})
        try:
            return r.json()["submission_id"]
        except:
            return -1

    def submit_problem(self, lang: str, problem: Problem, code: str) -> int:
        return self.submit(lang, problem.id, problem.title_slug, code)

    def submission_status(self, submission_id: int) -> Submission:
        r = self.s.get(urls.SUBMISSION_STATUS % submission_id)
        try:
            return Submission(r.json())
        except:
            return Submission({})
