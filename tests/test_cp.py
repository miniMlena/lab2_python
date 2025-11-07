from pathlib import Path
import pytest
from pytest_mock import MockerFixture
from src.errors import ShellError
from src.cp import cp

def test_cp_invalid_option():
    with pytest.raises(ShellError):
        cp("-k")
        cp("-rn")


def test_cp_no_arguments():
    with pytest.raises(ShellError):
        cp('')


def test_cp_too_little_arguments():
    with pytest.raises(ShellError):
        cp('only/one/path')


def test_cp_too_many_arguments():
    with pytest.raises(ShellError):
        cp('-r path/to/"file 1" path/to/file2 path/to/dir')
        cp('"path/to/my file" dir1 dir2')


def test_cp_nonexistent_source(mocker: MockerFixture):
    source_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    source_mock.exists.return_value = False
        
    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
        
    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: source_mock if x == "nonexistent.txt" else dest_mock
        
    with pytest.raises(ShellError):
        cp("nonexistent.txt target.txt")

    assert fake_path_class.call_count == 2
    source_mock.exists.assert_called_once()


def test_cp_directory_without_r_option(mocker: MockerFixture):
    source_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    source_mock.exists.return_value = True
    source_mock.is_dir.return_value = True
        
    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dest_mock.exists.return_value = True
        
    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: source_mock if x == "source/dir" else dest_mock
        
    with pytest.raises(ShellError):
        cp("source/dir target/dir")

    assert fake_path_class.call_count == 2
    source_mock.exists.assert_called_once()
    source_mock.is_dir.assert_called_once()


def test_cp_parent_directory_not_exists(mocker: MockerFixture):
    source_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    source_mock.exists.return_value = True
    source_mock.is_file.return_value = True
    source_mock.is_dir.return_value = False
        
    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dest_mock.exists.return_value = False
    dest_mock.is_file.return_value = True
    dest_mock.is_dir.return_value = False
    dest_mock.parent.exists.return_value = False  # Родительская директория не существует

    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: source_mock if x == "source.txt" else dest_mock
        
    with pytest.raises(ShellError):
        cp("source.txt nonexistent/destination.txt")
        
    assert fake_path_class.call_count == 2
    dest_mock.parent.exists.assert_called_once()



def test_cp_file_to_file(mocker: MockerFixture):
    source_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    source_mock.exists.return_value = True
    source_mock.is_file.return_value = True
    source_mock.is_dir.return_value = False
        
    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dest_mock.exists.return_value = False
    dest_mock.is_dir.return_value = False
    dest_mock.parent.exists.return_value = True
        
    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: source_mock if x == "source.txt" else dest_mock
        
    mock_copy2 = mocker.patch('shutil.copy2')

    cp("source.txt destination.txt")

    assert fake_path_class.call_count == 2
    fake_path_class.assert_any_call("source.txt")
    fake_path_class.assert_any_call("destination.txt")
    source_mock.exists.assert_called_once()
    source_mock.is_dir.assert_called()
    dest_mock.parent.exists.assert_called_once()
    mock_copy2.assert_called_once_with(source_mock, dest_mock)



def test_cp_file_to_existing_directory(mocker: MockerFixture):
    source_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    source_mock.exists.return_value = True
    source_mock.is_file.return_value = True
    source_mock.is_dir.return_value = False
    source_mock.name = "file.txt"

    dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    dest_mock.exists.return_value = True
    dest_mock.is_dir.return_value = True
        
    final_dest_mock = mocker.create_autospec(Path, instance=True, spec_set=True)
    final_dest_mock.parent.exists.return_value = True
        
    dest_mock.__truediv__.return_value = final_dest_mock
        
    fake_path_class = mocker.patch('src.paths.Path')
    fake_path_class.side_effect = lambda x: source_mock if x == "file.txt" else dest_mock
        
    mock_copy2 = mocker.patch('shutil.copy2')
        
    cp("file.txt target_dir")
        
    assert fake_path_class.call_count == 2
    dest_mock.__truediv__.assert_called_with("file.txt")
    mock_copy2.assert_called_once_with(source_mock, final_dest_mock)