from typing import List

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
        csrf = self.s.cookies.get("csrftoken")
        body = """{"query":"query getQuestionDetail($titleSlug: String!) {\\n  question(titleSlug: $titleSlug) {\\n    questionId\\n    questionTitle\\n    content\\n    difficulty\\n    stats\\n    contributors\\n    companyTags\\n    topicTags\\n    similarQuestions\\n    discussUrl\\n    libraryUrl\\n    mysqlSchemas\\n    randomQuestionUrl\\n    sessionId\\n    categoryTitle\\n    submitUrl\\n    interpretUrl\\n    codeDefinition\\n    sampleTestCase\\n    enableTestMode\\n    metaData\\n    enableRunCode\\n    enableSubmit\\n    judgerAvailable\\n    emailVerified\\n    envInfo\\n    urlManager\\n    likesDislikes {\\n      likes\\n      dislikes\\n      __typename\\n    }\\n    article\\n    questionDetailUrl\\n    isLiked\\n    discussCategoryId\\n    nextChallengePairs\\n    __typename\\n  }}\\n","variables":{"titleSlug":"%s"},"operationName":"getQuestionDetail"}""" % question_slug
        r = self.s.post(urls.GRAPHQL,
                        data=body,
                        headers={"referer": urls.DESCRIPTION % question_slug,
                                 "X-CSRFToken": csrf,
                                 "Content-Type": "application/json"})
        d = {}
        try:
            d = r.json()["data"]["question"]
        except:
            pass
        return ProblemDetail(d or {})
