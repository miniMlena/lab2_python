import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from unittest.mock import Mock
from src.grep import grep
from src.errors import ShellError
import re

def test_grep_file_with_matches(mocker: MockerFixture):
    """Тест поиска в файле с совпадениями"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "test.txt"
    
    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.return_value = file_mock
    
    mock_file_content = "hello world\nthis is a test\ngoodbye world\n"
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_file_content))
    
    mock_print = mocker.patch('builtins.print')
    
    grep("hello test.txt")
    
    fake_path_class.assert_called_once_with("test.txt")
    file_mock.exists.assert_called_once()
    mock_open.assert_called_once_with(file_mock, 'r', encoding='utf-8')
    
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "test.txt" in output
    assert "hello world" in output

def test_grep_file_no_matches(mocker: MockerFixture):
    """Тест поиска в файле без совпадений"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "test.txt"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="no matches here\n"))
    mock_print = mocker.patch('builtins.print')
    
    grep("pattern test.txt")
    
    fake_path_class.assert_called_once_with("test.txt")
    mock_open.assert_called_once_with(file_mock, 'r', encoding='utf-8')
    mock_print.assert_not_called()

def test_grep_with_i_option(mocker: MockerFixture):
    """Тест поиска без учета регистра (-i)"""
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

def test_grep_directory_without_r_option(mocker: MockerFixture):
    """Тест поиска в директории без опции -r"""
    dir_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dir_mock.exists.return_value = True
    dir_mock.is_file.return_value = False
    dir_mock.is_dir.return_value = True
    dir_mock.__str__.return_value = "somedir"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=dir_mock)
    
    with pytest.raises(ShellError):
        grep("pattern somedir")
    
    fake_path_class.assert_called_once_with("somedir")

def test_grep_directory_with_r_option(mocker: MockerFixture):
    """Тест рекурсивного поиска в директории (-r)"""
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

def test_grep_nonexistent_file(mocker: MockerFixture):
    """Тест поиска в несуществующем файле"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = False
    file_mock.__str__.return_value = "nonexistent.txt"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    mock_print = mocker.patch('builtins.print')
    
    with pytest.raises(ShellError):
        grep("pattern nonexistent.txt")
    
    fake_path_class.assert_called_once_with("nonexistent.txt")
    file_mock.exists.assert_called_once()

def test_grep_permission_denied(mocker: MockerFixture):
    """Тест обработки ошибки прав доступа"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "restricted.txt"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    
    mock_open = mocker.patch('builtins.open', side_effect=PermissionError("Permission denied"))

    with pytest.raises(ShellError):
        grep("pattern restricted.txt")
    
    fake_path_class.assert_called_once_with("restricted.txt")

def test_grep_binary_file(mocker: MockerFixture):
    """Тест обработки бинарного файла"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "binary.bin"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    
    mock_open = mocker.patch('builtins.open', side_effect=UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid byte'))
    
    with pytest.raises(ShellError):
        grep("pattern binary.bin")
    
    fake_path_class.assert_called_once_with("binary.bin")

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
    """Тест комбинированных опций (-ri)"""
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

def test_grep_line_numbers_format(mocker: MockerFixture):
    """Тест формата вывода с номерами строк"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "test.txt"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="first line\nsecond line\npattern here\n"))
    mock_print = mocker.patch('builtins.print')
    
    grep("pattern test.txt")
    
    # Проверяем формат вывода: имя_файла : номер_строки : содержимое
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "test.txt : 3 : pattern here" in output

def test_grep_with_regex_special_chars(mocker: MockerFixture):
    """Тест поиска с специальными символами regex"""
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

def test_grep_with_dot_regex(mocker: MockerFixture):
    """Тест поиска с точкой в regex (любой символ)"""
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False
    file_mock.__str__.return_value = "test.txt"
    
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="aXc\naYc\naZc\n"))
    mock_print = mocker.patch('builtins.print')
    
    # a любой_символ c
    grep("a.c test.txt")
    
    assert mock_print.call_count == 3