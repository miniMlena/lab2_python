import re

COMMAND_RE: re.Pattern = re.compile(
    r"""
    \s*
    ([a-z]+)
    (?:\s+(-[a-zA-Z]+))?
    (?:\s+(.*))?   #ОН НЕ УБИРАЕТ ПРОБЕЛЫ В КОНЦЕ ПУТИ
    """,
      re.VERBOSE
      )

m = COMMAND_RE.search("ls -l    dajd  alfsnl    ")

print(m.group(1), m.group(2), m.group(3))

'''
def parse(text: str) -> list:
    # if not text:
        # обработать пустой ввод

    m = COMMAND_RE.match(text)
    '''