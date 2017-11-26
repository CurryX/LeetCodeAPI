import requests as requests
from . import urls


class LeetCodeSession:
    def __init__(self):
        self.s = requests.Session()

    def check_login(self) -> bool:
        r = self.s.get(urls.CHECKIN)
        try:
            msg = r.json()["msg"]
            return "log in" not in msg
        except:
            return False

    def login(self, username: str, password: str) -> bool:
        self.s.get(urls.LOGIN)
        csrf = self.s.cookies.get("csrftoken")
        self.s.post(urls.LOGIN, data={"login": username, "password": password, "remember": "on",
                                      "csrfmiddlewaretoken": csrf},
                    headers={"referer": urls.LOGIN})
        return self.check_login()
