import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, call
from src.history import history
from src.errors import ShellError

def test_history_default_count(mocker: MockerFixture):
    """Тест с количеством по умолчанию (10)"""
    mocker.patch('os.path.exists', return_value=True)

    mock_log_content = "ls\ncd /\ncat file.txt\ngrep pattern .\ncp file1 file2\nmv old new\nrm file.txt\nhistory\n"
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_log_content))

    mock_print = mocker.patch('builtins.print')

    history("")

    assert mock_print.call_count == 8
    first_call_args = mock_print.call_args_list[0][0]
    output = first_call_args[0]
    assert output.startswith("   1")

def test_history_with_custom_count(mocker: MockerFixture):
    """Тест с указанным количеством команд"""
    mocker.patch('os.path.exists', return_value=True)
    
    mock_log_content = "ls\ncd /\ncat file.txt\ngrep pattern .\ncp file1 file2\n"
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_log_content))
    mock_print = mocker.patch('builtins.print')

    history("3")
    
    mock_open.assert_called_once()
    assert mock_print.call_count == 3

def test_history_invalid_line_count(mocker: MockerFixture):
    """Обработка неверного количества строк"""
    mocker.patch('os.path.exists', return_value=True)

    with pytest.raises(ShellError):
        history("-5")

    with pytest.raises(ShellError) as exc_info:
        history("0")
    
    with pytest.raises(ShellError) as exc_info:
        history("abc")