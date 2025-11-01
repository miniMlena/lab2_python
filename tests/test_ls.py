from pathlib import Path
from unittest.mock import Mock
import pytest
from pytest_mock import MockerFixture
from src.errors import ShellError
from src.ls import ls

def test_ls_invalid_option():
    with pytest.raises(ShellError):
        ls("-k")
        ls("-ln")

def test_ls_too_many_arguments():
    with pytest.raises(ShellError):
        ls('-l path/to/"file 1" path/to/file2')
        ls("path/to/my file")

def test_ls_called_for_nonexisted_folder(mocker: MockerFixture):
    fake_path_object: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    fake_path_object.exists.return_value = False
    nonexistent_path: str = "nonexistent"

    fake_path_class = mocker.patch('src.paths.Path', return_value=fake_path_object)

    with pytest.raises(ShellError):
        ls(nonexistent_path)

    fake_path_class.assert_called_once_with(nonexistent_path)    # Прошла нормализация пути
    fake_path_object.exists.assert_called_once()    # Была проверка существования пути
    fake_path_object.is_file.assert_not_called()    # Следующие строки кода не выполнялись

def test_ls_called_for_existing_directory(mocker: MockerFixture):
    path_object: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    path_object.exists.return_value = True
    path_object.is_file.return_value = False

    entry = mocker.Mock()
    entry.name = "file.txt"
    path_object.iterdir.return_value = [entry]

    fake_path_class = mocker.patch('src.paths.Path', return_value=path_object)
    mock_print = mocker.patch('builtins.print')
            
    ls("fake/dir")

    fake_path_class.assert_called_once_with("fake/dir")
    path_object.exists.assert_called_once()
    path_object.is_file.assert_called_once()
    path_object.iterdir.assert_called_once()
    mock_print.assert_called_with("file.txt")