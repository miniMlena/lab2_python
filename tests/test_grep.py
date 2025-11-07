import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from unittest.mock import Mock
from src.grep import grep
from src.errors import ShellError

def test_grep_file_no_matches(mocker: MockerFixture):
    """Тест поиска в файле без совпадений"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="no matches here\n"))
    mock_print = mocker.patch('builtins.print')
    
    grep("pattern test.txt")
    
    fake_path_class.assert_called_once_with("test.txt")
    mock_open.assert_called_once_with(file_mock, 'r', encoding='utf-8')
    mock_print.assert_not_called()


def test_grep_with_i_option(mocker: MockerFixture):
    """Тест поиска с опцией -i"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "test.txt"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="HELLO world\n"))
    mock_print = mocker.patch('builtins.print')
    
    grep("-i hello test.txt")
    
    fake_path_class.assert_called_once_with("test.txt")
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "HELLO world" in output


def test_grep_directory_with_r_option(mocker: MockerFixture):
    """Тест рекурсивного поиска в директории"""
    dir_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dir_mock.exists.return_value = True
    dir_mock.is_file.return_value = False
    dir_mock.is_dir.return_value = True
    dir_mock.__str__.return_value = "somedir"
    
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "somedir/file.txt"
    
    dir_mock.iterdir.return_value = [file_mock]
    
    fake_path_class = mocker.patch('src.paths.Path')
    def path_side_effect(arg):
        if arg == "somedir":
            return dir_mock
        elif arg == "somedir/file.txt":
            return file_mock
        return Mock()
    fake_path_class.side_effect = path_side_effect
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="pattern found\n"))
    mock_print = mocker.patch('builtins.print')
    
    grep("-r pattern somedir")
    
    dir_mock.iterdir.assert_called_once()
    mock_print.assert_called_once()


def test_grep_invalid_pattern(mocker: MockerFixture):
    """Тест обработки неверного шаблона"""
    with pytest.raises(ShellError):
        grep("[invalid test.txt")
    

def test_grep_multiple_files(mocker: MockerFixture):
    """Тест поиска в нескольких файлах"""
    file1_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file1_mock.exists.return_value = True
    file1_mock.is_file.return_value = True
    file1_mock.is_dir.return_value = False
    file1_mock.__str__.return_value = "file1.txt"
    
    file2_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file2_mock.exists.return_value = True
    file2_mock.is_file.return_value = True
    file2_mock.is_dir.return_value = False
    file2_mock.__str__.return_value = "file2.txt"
    
    fake_path_class = mocker.patch('src.paths.Path')
    def path_side_effect(arg):
        if arg == "file1.txt":
            return file1_mock
        elif arg == "file2.txt":
            return file2_mock
        return Mock()
    fake_path_class.side_effect = path_side_effect

    mock_open = mocker.patch('builtins.open')
    mock_open.side_effect = [
        mocker.mock_open(read_data="pattern in file1\n").return_value,
        mocker.mock_open(read_data="no match here\n").return_value
    ]
    
    mock_print = mocker.patch('builtins.print')
    
    grep("pattern file1.txt file2.txt")

    assert fake_path_class.call_count == 2
    assert mock_open.call_count == 2
    
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "file1.txt" in output

def test_grep_combined_options(mocker: MockerFixture):
    """Тест с опциями -ri"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "test.txt"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="PATTERN found\n"))
    mock_print = mocker.patch('builtins.print')
    
    grep("-ri pattern test.txt")
    
    fake_path_class.assert_called_once_with("test.txt")
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "PATTERN found" in output

def test_grep_no_arguments():
    """Тест вызова grep без аргументов"""
    with pytest.raises(ShellError):
        grep("")

def test_grep_missing_file_operand():
    """Тест вызова grep без указания файла"""
    with pytest.raises(ShellError):
        grep("pattern")


def test_grep_with_regex_special_chars(mocker: MockerFixture):
    """Тест поиска со специальными символами"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "test.txt"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="test123\nabc.def\n"))
    mock_print = mocker.patch('builtins.print')

    grep(r"\d+ test.txt")
    
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "test123" in output