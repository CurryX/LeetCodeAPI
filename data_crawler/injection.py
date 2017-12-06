import re


injected = []


def inject(src: str, func: str, count: int) -> str:
    lines = src.splitlines()
    lines.insert(0, "xxx_counter = 0")
    for i in range(len(lines)):
        if re.match(r"^\s*def\s+" + func + r"\(", lines[i]):
            indent = ""
            for j in range(i + 1, len(lines)):
                m = re.match(r"^(\s+)\S", lines[j])
                if m:
                    indent = m.group(1)
                    break
            lines.insert(i + 1, "%sprint(locals()); global xxx_counter; xxx_counter += 1" % indent)
            lines.insert(i + 2, "%sif xxx_counter >= %d: return" % (indent, count))
            break
    return "\r\n".join(lines)
