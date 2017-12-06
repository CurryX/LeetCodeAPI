from typing import Dict


class Problem:
    def __init__(self, dic: Dict[str, object]):
        self.level: int = dic.get("difficulty", {}).get("level", 0)
        self.frequency: float = dic.get("frequency", 0.0)
        self.paid_only: bool = dic.get("paid_only", False)
        self.status: str = dic.get("status", None)
        stat: Dict[str, object] = dic.get("stat", {})
        self.is_new: bool = stat.get("is_new_question", False)
        self.title: str = stat.get("question__title", None)
        self.title_slug: str = stat.get("question__title_slug", None)
        self.article_slug: str = stat.get("question__article_slug", None)
        self.id: int = stat.get("question_id", 0)
        self.total_acs: int = stat.get("total_acs", 0)
        self.total_submitted: int = stat.get("total_submitted", 0)


class Submission:
    def __init__(self, dic: Dict[str, object]):
        self.total_testcases: int = dic.get("total_testcases", 0)
        self.total_correct: int = dic.get("total_correct", 0)
        self.stderr: str = dic.get("code_output", None)
        self.stdout: str = dic.get("std_output", None)
        self.status_code: int = dic.get("status_code", 0)
        self.status_msg: str = dic.get("status_msg", None)
        self.state: str = dic.get("state", None)
        self.status_runtime: str = dic.get("status_runtime", None)
        self.question_id: str = dic.get("question_id", None)
        self.lang: str = dic.get("lang", None)


class ProblemDetail:
    class DefaultCode:
        def __init__(self, dic: Dict[str, object]):
            self.lang = dic.get("text", None)
            self.code = dic.get("defaultCode", None)

    def __init__(self, dic: Dict[str, object], description: str):
        self.category = dic.get("categoryTitle", None)
        self.description = description
        self.default_codes: Dict[str, ProblemDetail.DefaultCode] = {}
        for e in dic.get("codeDefinition", []):
            self.default_codes[e["value"]] = ProblemDetail.DefaultCode(e)
