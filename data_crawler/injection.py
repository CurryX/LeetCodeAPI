import re
from typing import List


def inject(src: str, funcs: List[str], count: int) -> str:
    lines = src.splitlines()
    lines.insert(0, "xxx_counter = 0")
    for i in range(len(lines)):
        for f in funcs:
            if re.match(r"^\s*def\s+" + f + r"\(", lines[i]):
                indent = ""
                for j in range(i + 1, len(lines)):
                    m = re.match(r"^(\s+)\S", lines[j])
                    if m:
                        indent = m.group(1)
                        break
                lines.insert(i + 1, "%sprint(locals()); global xxx_counter; xxx_counter += 1" % indent)
                lines.insert(i + 2, "%sif xxx_counter >= %d: return" % (indent, count * len(funcs)))
                break
    return "\r\n".join(lines)


def find_funcs(src: str) -> List[str]:
    funcs = []
    for line in src.splitlines():
        m = re.match(r"^\s*def\s([\w_]+)\(", line)
        if m:
            funcs.append(m.group(1))
    return funcs
