from pathlib import Path
import pytest
from pytest_mock import MockerFixture
from src.undo_logging import log_remove, log_copy, log_move, remove_error_from_trash

def test_log_remove_directory(mocker: MockerFixture):
    """Тест логирования удаления директории"""
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.is_file.return_value = False
    mock_path.is_dir.return_value = True
    
    mock_logger = mocker.patch('src.undo_logging.undo_logger')
    
    file1 = mocker.MagicMock(spec=Path)
    file1.is_file.return_value = True
    file1.is_dir.return_value = False
    file1.relative_to.return_value = "file1.txt"
    
    dir1 = mocker.MagicMock(spec=Path)
    dir1.is_file.return_value = False
    dir1.is_dir.return_value = True
    dir1.relative_to.return_value = "subdir"
    
    file2 = mocker.MagicMock(spec=Path)
    file2.is_file.return_value = True
    file2.is_dir.return_value = False
    file2.relative_to.return_value = "subdir/file2.txt"
    
    mock_path.rglob.return_value = [file1, dir1, file2]
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='file content'))
    
    log_remove(mock_path)
    
    expected_calls = [
        mocker.call(f"rm_dir path:{mock_path}"),
        mocker.call("file:file1.txt content:file content"),
        mocker.call("dir:subdir"),
        mocker.call("file:subdir/file2.txt content:file content"),
        mocker.call("---END_DIR---")
    ]
    mock_logger.info.assert_has_calls(expected_calls)


def test_log_copy_file(mocker: MockerFixture):
    """Тест логирования копирования файла"""
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mock_path.is_dir.return_value = False
    
    mock_logger = mocker.patch('src.undo_logging.undo_logger')
    
    log_copy(mock_path)
    
    mock_logger.info.assert_called_once_with(f"cp_file dest:{mock_path}")


def test_log_move_directory(mocker: MockerFixture):
    """Тест логирования перемещения директории"""
    mock_source = mocker.MagicMock(spec=Path)
    mock_dest = mocker.MagicMock(spec=Path)
    mock_source.is_file.return_value = False
    mock_source.is_dir.return_value = True
    
    mock_logger = mocker.patch('src.undo_logging.undo_logger')
    
    log_move(mock_source, mock_dest)
    
    mock_logger.info.assert_called_once_with(f"mv_dir source:{mock_source} dest:{mock_dest}")


def test_remove_error_from_trash_success(mocker: MockerFixture):
    """Тест удаления ошибочной операции из trash файла"""
    mock_trash_content = [
        "rm_file path:/file1.txt content:content1\n",
        "rm_file path:/file2.txt content:content2\n",
        "cp_file dest:/copy.txt\n"
    ]
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=''.join(mock_trash_content)))
    
    remove_error_from_trash()
    
    mock_open().writelines.assert_called_once_with([
        "rm_file path:/file1.txt content:content1\n",
        "rm_file path:/file2.txt content:content2\n"
    ])