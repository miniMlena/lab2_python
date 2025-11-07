from pathlib import Path
from unittest.mock import Mock
import pytest
from pytest_mock import MockerFixture
from src.errors import ShellError
from src.cat import cat

def test_cat_no_arguments():
    with pytest.raises(ShellError):
        cat('')

def test_cat_too_many_arguments():
    with pytest.raises(ShellError):
        cat('path/to/"file 1" path/to/file2')
        cat("path/to/my file")

def test_cat_called_for_nonexisted_file(mocker: MockerFixture):
    fake_path_object: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    fake_path_object.exists.return_value = False
    nonexistent_path: str = "nonexistent.txt"

    fake_path_class = mocker.patch('src.paths.Path', return_value=fake_path_object)

    with pytest.raises(ShellError):
        cat(nonexistent_path)

    fake_path_class.assert_called_once_with(nonexistent_path)    # Прошла нормализация пути
    fake_path_object.exists.assert_called_once()    # Была проверка существования пути
    fake_path_object.is_dir.assert_not_called()    # Следующие строки кода не выполнялись

def test_cat_called_for_directory(mocker: MockerFixture):
    path_obj: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    path_obj.exists.return_value = True
    path_obj.is_dir.return_value = True

    fake_path_class = mocker.patch('src.paths.Path', return_value=path_obj)

    with pytest.raises(ShellError):
        cat("directory")

    fake_path_class.assert_called_once_with("directory")
    path_obj.exists.assert_called_once()    # Была проверка существования пути
    path_obj.is_dir.assert_called_once()    # Была проверка, является ли путь директорией

def test_cat_permission_denied(mocker: MockerFixture):
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_dir.return_value = False

    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)
    
    mocker.patch('os.access', return_value=False)

    with pytest.raises(ShellError):
        cat('"no permission.txt"')

    fake_path_class.assert_called_once_with("no permission.txt")
    file_mock.exists.assert_called_once()
    file_mock.is_dir.assert_called_once()

def test_cat_called_for_existing_file(mocker: MockerFixture):
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_dir.return_value = False

    mocker.patch('os.access', return_value=True)
        
    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)

    mock_file_content = "Hello, World!\nThis is a test file."
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_file_content))

    mock_print = mocker.patch('builtins.print')

    cat("file.txt")
 
    fake_path_class.assert_called_once_with("file.txt")
    mock_open.assert_called_once_with(file_mock, 'r', encoding='utf-8')
    mock_print.assert_called_once_with(mock_file_content, end='')