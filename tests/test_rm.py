from pathlib import Path
import pytest
from pytest_mock import MockerFixture
from src.errors import ShellError
from src.rm import rm


def test_rm_no_arguments():
    with pytest.raises(ShellError):
        rm('')


def test_rm_too_little_arguments():
    with pytest.raises(ShellError):
        rm('only/one/path')


def test_rm_too_many_arguments():
    with pytest.raises(ShellError):
        rm('-r path/to/"file 1" path/to/file2 path/to/dir')
        rm('"path/to/my file" dir1 dir2')


def test_rm_nonexistent_source(mocker: MockerFixture):
    fake_path_object = mocker.create_autospec(Path, instance=True, spec_set=True)
    fake_path_object.exists.return_value = False
    nonexistent_path: str = "nonexistent"

    fake_path_class = mocker.patch('src.paths.Path', return_value=fake_path_object)

    with pytest.raises(ShellError):
        rm(nonexistent_path)

    fake_path_class.assert_called_once_with(nonexistent_path)
    fake_path_object.exists.assert_called_once()



def test_rm_directory_without_r_option(mocker: MockerFixture):
    dir_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dir_mock.exists.return_value = True
    dir_mock.is_file.return_value = False
    dir_mock.is_dir.return_value = True

    fake_path_class = mocker.patch('src.paths.Path', return_value=dir_mock)
        
    with pytest.raises(ShellError):
        rm("somedir")

    fake_path_class.assert_called_once_with("somedir")
    dir_mock.exists.assert_called_once()
    dir_mock.is_dir.assert_called_once()



def test_rm_root_directory_protection(mocker: MockerFixture):
    root_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    root_mock.exists.return_value = True
    root_mock.is_dir.return_value = True

    root_mock.parent = root_mock

    fake_path_class = mocker.patch('src.paths.Path', return_value=root_mock)
        
    with pytest.raises(ShellError):
        rm("-r /")

    fake_path_class.assert_called_once_with("/")



def test_rm_file(mocker: MockerFixture):
    file_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    file_mock.exists.return_value = True
    file_mock.is_file.return_value = True
    file_mock.is_dir.return_value = False

    fake_path_class = mocker.patch('src.paths.Path', return_value=file_mock)

    mock_remove = mocker.patch('os.remove')

    rm("file.txt")

    fake_path_class.assert_called_once_with("file.txt")
    file_mock.exists.assert_called_once()
    file_mock.is_dir.assert_called()
    mock_remove.assert_called_once_with(file_mock)



def test_rm_directory_with_r_and_confirmation(mocker: MockerFixture):
    dir_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dir_mock.exists.return_value = True
    dir_mock.is_file.return_value = False
    dir_mock.is_dir.return_value = True

    fake_path_class = mocker.patch('src.paths.Path', return_value=dir_mock)

    mock_input = mocker.patch('builtins.input', return_value="y")

    mock_rmtree = mocker.patch('shutil.rmtree')

    rm("-r somedir")

    fake_path_class.assert_called_once_with("somedir")
    dir_mock.exists.assert_called_once()
    dir_mock.is_dir.assert_called()
    mock_input.assert_called_once()
    mock_rmtree.assert_called_once_with(dir_mock)
    


def test_rm_directory_with_r_and_rejection(mocker: MockerFixture):
    dir_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dir_mock.exists.return_value = True
    dir_mock.is_file.return_value = False
    dir_mock.is_dir.return_value = True

    fake_path_class = mocker.patch('src.paths.Path', return_value=dir_mock)

    mock_input = mocker.patch('builtins.input', return_value="n")

    mock_rmtree = mocker.patch('shutil.rmtree')

    rm("-r somedir")

    fake_path_class.assert_called_once_with("somedir")
    dir_mock.exists.assert_called_once()
    dir_mock.is_dir.assert_called()
    mock_input.assert_called_once()
    mock_rmtree.assert_not_called()