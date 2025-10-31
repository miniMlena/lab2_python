import re

PATH_RE: re.Pattern = re.compile(
    r"""
    (?:[^\s"]*\\?["][^\\"]*\s+[^\\"]*["]\\?[^\s"]*)+
    |[^\s]+
    """,
    re.VERBOSE
)

COMMAND_RE: re.Pattern = re.compile(
    r"""
\s*
([^\s]+)
(?:\s+-([^\s]+))?
(?:\s+(.*))?
""",
    re.VERBOSE
)

NEW_COMMAND_RE: re.Pattern = re.compile(
    r"""
\s*
([^\s]+)
(?:\s+-([^\s]+))?
(?:(?:\s+([^\s]+))|(?:\s+('.+')))?
""",
    re.VERBOSE
)