from src.constants import NEW_COMMAND_RE

def parse(text: str) -> list | None:
    if text.strip():
        # обработать пустой ввод?
        text.replace('"', "'")
        m = NEW_COMMAND_RE.search(text.strip())
        return [m.group(1), m.group(2), m.group(3), m.group(4)]

#print(parse(" lsl  'fs dfgdf' "))



import re
EXPERIMENT_RE = re.compile(
    r"""
(?:\s+'(.+)')|(?:\s+([^\s]+))
""",
    re.VERBOSE
)

text = " adjmtor 'ajkas  dj'  "
m = EXPERIMENT_RE.search(text.strip())
print(m)
print("   ls -l      'yjdfz gfgrf'      ".split())