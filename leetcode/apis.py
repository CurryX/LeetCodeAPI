from typing import List

import js2py
from bs4 import BeautifulSoup

from . import urls
from .session import LeetCodeSession
from .models import Problem, Submission, ProblemDetail


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

    def submission_status(self, submission_id: int) -> Submission:
        r = self.s.get(urls.SUBMISSION_STATUS % submission_id)
        try:
            return Submission(r.json())
        except:
            return Submission({})

    def get_problem_detail(self, question_slug: str) -> ProblemDetail:
        html = self.s.get(urls.DESCRIPTION % question_slug).text
        doc = BeautifulSoup(html, "html5lib")
        element = doc.find(class_="question-description")
        if not element:
            return ProblemDetail({}, "")
        description = element.get_text()
        page_data = {}
        for e in doc.find_all("script"):
            s = e.get_text()
            if "var pageData" in s:
                s += "; pageData"
                page_data = js2py.eval_js(s).to_dict()
                break
        return ProblemDetail(page_data, description)
