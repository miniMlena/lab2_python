import pytest
from src.errors import ShellError
from src.execute import execute

def test_execute_command_not_found():
    with pytest.raises(ShellError):
        execute('chdir ~')
        execute('ls-l .')