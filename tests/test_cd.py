from pathlib import Path
from unittest.mock import Mock
import pytest
from pytest_mock import MockerFixture
from src.errors import ShellError
from src.cd import cd

def test_cd_too_many_arguments():
    with pytest.raises(ShellError):
        cd('path/to/"file 1" path/to/file2')
        cd("path/to/my file")

def test_cd_called_for_nonexisted_folder(mocker: MockerFixture):
    fake_path_object: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    fake_path_object.exists.return_value = False
    nonexistent_path: str = "nonexistent"

    fake_path_class = mocker.patch('src.paths.Path', return_value=fake_path_object)

    with pytest.raises(ShellError):
        cd(nonexistent_path)

    fake_path_class.assert_called_once_with(nonexistent_path)    # Прошла нормализация пути
    fake_path_object.exists.assert_called_once()    # Была проверка существования пути
    fake_path_object.is_dir.assert_not_called()    # Следующие строки кода не выполнялись

def test_cd_called_for_file(mocker: MockerFixture):
    path_obj: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    path_obj.exists.return_value = True
    path_obj.is_dir.return_value = False

    fake_path_class = mocker.patch('src.paths.Path', return_value=path_obj)

    with pytest.raises(ShellError):
        cd("file.txt")

    fake_path_class.assert_called_once_with("file.txt")    # Прошла нормализация пути
    path_obj.exists.assert_called_once()    # Была проверка существования пути
    path_obj.is_dir.assert_called_once()    # Была проверка, является ли путь директорией

def test_cd_called_for_existing_absolut_path(mocker: MockerFixture):
    path_object: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    path_object.exists.return_value = True
    path_object.is_dir.return_value = True

    fake_path_class = mocker.patch('src.paths.Path', return_value=path_object)
    mock_chdir = mocker.patch('os.chdir')

    cd("/fake/dir")

    fake_path_class.assert_called_once_with("/fake/dir")
    path_object.exists.assert_called_once()
    path_object.is_dir.assert_called_once()
    mock_chdir.assert_called_once_with(path_object)

def test_cd_called_for_home_directory(mocker: MockerFixture):
    home_mock: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)

    fake_path_class = mocker.patch('src.cd.Path')
    fake_path_class.home.return_value = home_mock

    mock_chdir = mocker.patch('os.chdir')

    cd("")

    fake_path_class.home.assert_called_once()
    home_mock.exists.assert_called_once()
    home_mock.is_dir.assert_called_once()
    mock_chdir.assert_called_once_with(home_mock)

def test_cd_called_for_relative_path(mocker: MockerFixture):
    cwd_mock = mocker.create_autospec(Path, instance=True, spec_set=True)

    relative_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    relative_mock.is_absolute.return_value = False
    
    absolute_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    absolute_mock.exists.return_value = True
    absolute_mock.is_dir.return_value = True
    
    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.return_value = relative_mock  # relative_mock = Path("subfolder")
    fake_path_class.cwd.return_value = cwd_mock 
    cwd_mock.__truediv__.return_value = absolute_mock # absolute_mock = cwd / relative_mock
    
    mock_chdir = mocker.patch('os.chdir')
    
    cd("subfolder")
    
    fake_path_class.assert_any_call("subfolder")
    fake_path_class.cwd.assert_called_once()      # Был вызов текущей директории
    cwd_mock.__truediv__.assert_called_once_with(relative_mock) # относительный путь преобразован в абсолютный
    absolute_mock.exists.assert_called_once()
    absolute_mock.is_dir.assert_called_once()
    mock_chdir.assert_called_once_with(absolute_mock)    # chdir получил в аргументе абсолютный путь