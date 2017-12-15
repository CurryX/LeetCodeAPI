import re
from typing import List


def inject(src: str, funcs: List[str], total: int) -> str:
    lines = src.splitlines()
    lines.insert(0, "xxx_counter = 0; xxx_buf = []; xxx_total = %d; xxx_segment = 0" % total)
    for i in range(len(lines)):
        for f in funcs:
            if re.match(r"^\s*def\s+" + f + r"\(", lines[i]):
                indent = ""
                for j in range(i + 1, len(lines)):
                    m = re.match(r"^(\s+)\S", lines[j])
                    if m:
                        indent = m.group(1)
                        break
                lines.insert(i + 1, "%sglobal xxx_counter, xxx_buf, xxx_total, xxx_segment; xxx_d = locals(); del "
                                    "xxx_d['self']; xxx_buf.append(xxx_d); xxx_counter += 1" % indent)
                lines.insert(i + 2, "%sif xxx_counter == xxx_total: print(str(xxx_buf)[xxx_segment * 1000000: "
                                    "(xxx_segment + 1) * 1000000]); return" % indent)
    return "\r\n".join(lines)


def find_funcs(src: str) -> List[str]:
    funcs = []
    for line in src.splitlines():
        m = re.match(r"^\s*def\s([\w_]+)\(", line)
        if m:
            funcs.append(m.group(1))
    return funcs
