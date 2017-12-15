import sys, os

import time

from data_crawler.injection import inject, find_funcs
from leetcode.apis import LeetCodeClient
from leetcode.models import Problem


submission_interval = 10
submission_count = 3
wait_interval = 2
wait_count = 10


def crawl(problem: Problem, default_code: str, path: str, file: str) -> None:
    print("Begin crawling %d: %s (%s)" % (problem.id, problem.title, problem.title_slug))
    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
        src = f.read()
    funcs = find_funcs(default_code)
    id = c.submit("python", problem.id, problem.title_slug, src)
    if id <= 0:
        print("Submission failed.")
        return
    for i in range(wait_count):
        time.sleep(wait_interval)
        submission = c.submission_status(id)
        if submission.state == "SUCCESS":
            break
        if submission.state == "FAILURE":
            print("Test failed.")
            return
    else:
        print("Wait timeout.")
        return
    if submission.status_msg != "Accepted":
        print("Submission status %s" % submission.status_msg)
        return
    total = submission.total_testcases
    print("Original code OK, total %d test cases." % total)
    for j in range(submission_count):
        time.sleep(submission_interval)
        id = c.submit("python", problem.id, problem.title_slug, inject(src, funcs, total))
        if id > 0:
            break
    else:
        print("Submission failed.")
        return
    for j in range(wait_count):
        time.sleep(wait_interval)
        submission = c.submission_status(id)
        if submission.state == "SUCCESS":
            break
        if submission.state == "FAILURE":
            print("Test failed.")
            return
    else:
        print("Wait timeout.")
        return
    with open(os.path.join(path, "%d.in" % problem.id), "w") as f:
        f.write(submission.stdout)
    print("End crawling %d: %s (%s)" % (problem.id, problem.title, problem.title_slug))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: %s <data_dir> <username> <password>" % sys.argv[0])
        exit()
    c = LeetCodeClient()
    if not c.login(sys.argv[2], sys.argv[3]):
        print("Login failed.")
        exit()
    problems = c.get_problems()
    path = sys.argv[1]
    for file in os.listdir(path):
        if file.endswith(".py"):
            name = file[0: len(file) - 3]
            for p in problems:
                if str(p.id) == name or p.title_slug == name:
                    d = c.get_problem_detail(p.title_slug)
                    if not "python" in d.default_codes:
                        print("python not in default codes for %s." % p.title_slug)
                    else:
                        crawl(p, d.default_codes["python"].code, path, file)
                        time.sleep(submission_interval)
                    break
