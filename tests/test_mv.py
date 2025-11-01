from pathlib import Path
import pytest
from pytest_mock import MockerFixture
from src.errors import ShellError
from src.mv import mv


def test_mv_no_arguments():
    with pytest.raises(ShellError):
        mv('')


def test_mv_too_little_arguments():
    with pytest.raises(ShellError):
        mv('only/one/path')


def test_mv_too_many_arguments():
    with pytest.raises(ShellError):
        mv('-r path/to/"file 1" path/to/file2 path/to/dir')
        mv('"path/to/my file" dir1 dir2')



def test_mv_nonexistent_source(mocker: MockerFixture):
    source_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    source_mock.exists.return_value = False
        
    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
        
    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: source_mock if x == "nonexistent.txt" else dest_mock
        
    with pytest.raises(ShellError):
        mv("nonexistent.txt target.txt")

    assert fake_path_class.call_count == 2
    source_mock.exists.assert_called_once()



def test_mv_directory_to_file(mocker: MockerFixture):
    src_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    src_mock.exists.return_value = True
    src_mock.is_file.return_value = False
    src_mock.is_dir.return_value = True
        
    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dest_mock.exists.return_value = True
    dest_mock.is_dir.return_value = False
        
    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: src_mock if x == "somedir" else dest_mock

    with pytest.raises(ShellError):
        mv("somedir somefile.txt")
        
    assert fake_path_class.call_count == 2
    src_mock.exists.assert_called_once()
    src_mock.is_dir.assert_called_once()
    dest_mock.exists.assert_called_once()
    dest_mock.is_dir.assert_called_once()



def test_mv_directory(mocker: MockerFixture):
    src_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    src_mock.exists.return_value = True
    src_mock.is_file.return_value = False
    src_mock.is_dir.return_value = True
    src_mock.is_relative_to.return_value = False
    
    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dest_mock.exists.return_value = False
    dest_mock.is_dir.return_value = False
    dest_mock.parent.exists.return_value = True
    dest_mock.is_relative_to.return_value = False

    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: src_mock if x == "sourcedir" else dest_mock

    mock_move = mocker.patch('shutil.move')

    mv("sourcedir targetdir")

    assert fake_path_class.call_count == 2
    src_mock.exists.assert_called()
    src_mock.is_dir.assert_called()
    dest_mock.parent.exists.assert_called_once()
    mock_move.assert_called_once_with(str(src_mock), str(dest_mock))


def test_mv_file_to_nonexistent_directory(mocker: MockerFixture):
    src_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    src_mock.exists.return_value = True
    src_mock.is_file.return_value = True
    src_mock.is_dir.return_value = False
    src_mock.name = "file.txt"
    
    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dest_mock.exists.return_value = False
    dest_mock.is_dir.return_value = False
    dest_mock.parent.exists.return_value = True

    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: src_mock if x == "file.txt" else dest_mock

    mock_move = mocker.patch('shutil.move')
    
    mv("file.txt newdir")

    assert fake_path_class.call_count == 2
    mock_move.assert_called_once_with(str(src_mock), str(dest_mock))