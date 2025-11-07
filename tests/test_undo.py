from pathlib import Path
import pytest
from pytest_mock import MockerFixture
from src.errors import ShellError
from src.undo import undo

def test_undo_empty_trash_file(mocker: MockerFixture):
    """Тест отмены при пустом trash файле"""
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mocker.patch('src.undo.trash_file', mock_path)
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=''))
    
    with pytest.raises(ShellError):
        undo()


def test_undo_rm_file(mocker: MockerFixture):
    """Тест отмены удаления файла"""
    mock_trash_content = "rm_file path:/test/file.txt content:Hello\\nWorld\n"
    
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mocker.patch('src.undo.trash_file', mock_path)
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_trash_content))
    
    mock_file_path = mocker.MagicMock(spec=Path)
    mock_parent = mocker.MagicMock(spec=Path)
    mock_parent.exists.return_value = False
    mock_file_path.parent = mock_parent
    
    mock_path_class = mocker.patch('src.undo.Path')
    mock_path_class.return_value = mock_file_path
    
    mock_remove_op = mocker.patch('src.undo.remove_operation_from_trash')
    
    undo()
    
    mock_path_class.assert_called_with("/test/file.txt")
    mock_parent.mkdir.assert_called_once_with(parents=True)
    mock_open().write.assert_called_once_with("Hello\nWorld")
    mock_remove_op.assert_called_once_with(0)


def test_undo_rm_dir(mocker: MockerFixture):
    """Тест отмены удаления директории"""
    mock_trash_content = "rm_dir path:/test/dir\n---END_DIR---\n"
    
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mocker.patch('src.undo.trash_file', mock_path)
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_trash_content))
    
    mock_dir_path = mocker.MagicMock(spec=Path)
    mock_path_class = mocker.patch('src.undo.Path', return_value=mock_dir_path)
    
    mock_remove_op = mocker.patch('src.undo.remove_operation_from_trash')
    
    undo()

    mock_path_class.assert_called_with("/test/dir")
    mock_dir_path.mkdir.assert_called_once()
    mock_remove_op.assert_called_once_with(0)


def test_undo_cp_file(mocker: MockerFixture):
    """Тест отмены копирования файла"""
    mock_trash_content = "cp_file dest:/copied/file.txt\n"
    
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mocker.patch('src.undo.trash_file', mock_path)
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_trash_content))
    
    mock_dest_path = mocker.MagicMock(spec=Path)
    mock_dest_path.exists.return_value = True
    
    mock_path_class = mocker.patch('src.undo.Path', return_value=mock_dest_path)
    
    mock_remove_op = mocker.patch('src.undo.remove_operation_from_trash')
    
    undo()
    
    mock_dest_path.unlink.assert_called_once()
    mock_remove_op.assert_called_once()


def test_undo_cp_dir(mocker: MockerFixture):
    """Тест отмены копирования директории"""
    mock_trash_content = "cp_dir dest:/copied/dir\n"
    
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mocker.patch('src.undo.trash_file', mock_path)
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_trash_content))
    
    mock_dest_path = mocker.MagicMock(spec=Path)
    mock_dest_path.exists.return_value = True
    
    mock_path_class = mocker.patch('src.undo.Path', return_value=mock_dest_path)
    
    mock_rmtree = mocker.patch('shutil.rmtree')
    
    mock_remove_op = mocker.patch('src.undo.remove_operation_from_trash')
    
    undo()
    
    mock_rmtree.assert_called_once_with(mock_dest_path)
    mock_remove_op.assert_called_once()


def test_undo_mv_file(mocker: MockerFixture):
    """Тест отмены перемещения файла"""
    mock_trash_content = "mv_file source:/old/file.txt dest:/new/file.txt\n"
    
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mocker.patch('src.undo.trash_file', mock_path)
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_trash_content))
    
    mock_source_path = mocker.MagicMock(spec=Path)
    mock_dest_path = mocker.MagicMock(spec=Path)
    mock_dest_path.exists.return_value = True
    
    mock_path_class = mocker.patch('src.undo.Path')
    mock_path_class.side_effect = [mock_source_path, mock_dest_path]
    
    mock_move = mocker.patch('shutil.move')
    
    mock_remove_op = mocker.patch('src.undo.remove_operation_from_trash')
    
    undo()
    
    mock_move.assert_called_once_with(mock_dest_path, mock_source_path)
    mock_remove_op.assert_called_once()


def test_undo_mv_dir(mocker: MockerFixture):
    """Тест отмены перемещения директории"""
    mock_trash_content = "mv_dir source:/old/dir dest:/new/dir\n"
    
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mocker.patch('src.undo.trash_file', mock_path)
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=mock_trash_content))
    
    mock_source_path = mocker.MagicMock(spec=Path)
    mock_dest_path = mocker.MagicMock(spec=Path)
    mock_dest_path.exists.return_value = True
    
    mock_path_class = mocker.patch('src.undo.Path')
    mock_path_class.side_effect = [mock_source_path, mock_dest_path]
    
    mock_move = mocker.patch('shutil.move')
    
    mock_remove_op = mocker.patch('src.undo.remove_operation_from_trash')
    
    undo()
    
    mock_move.assert_called_once_with(mock_dest_path, mock_source_path)
    mock_remove_op.assert_called_once()