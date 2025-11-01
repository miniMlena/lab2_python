import re

PATH_RE: re.Pattern = re.compile(
    r"""
    (?:[^\s"]*\\?["][^\\"]*\s+[^\\"]*["]\\?[^\s"]*)+
    |[^\s]+
    """,
    re.VERBOSE
)