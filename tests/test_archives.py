from pathlib import Path
import pytest
from pytest_mock import MockerFixture
from src.errors import ShellError
from src.zip import zip_command, unzip_command
from src.tar import tar_command, untar_command

def test_zip_command_file(mocker: MockerFixture):
    """Тест создания ZIP архива из файла"""
    mock_source = mocker.MagicMock(spec=Path)
    mock_source.exists.return_value = True
    mock_source.is_file.return_value = True
    mock_source.is_dir.return_value = False
    mock_source.name = 'test.txt'
    
    mock_archive = mocker.MagicMock(spec=Path)
    mock_archive.suffix = '.zip'
    
    mock_path_class = mocker.patch('src.paths.Path')
    mock_path_class.side_effect = [mock_source, mock_archive]
    
    mock_zipfile = mocker.patch('src.zip.zipfile.ZipFile')
    mock_zip_instance = mocker.MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
    
    zip_command("test.txt archive.zip")
    
    mock_source.exists.assert_called_once()
    mock_source.is_file.assert_called_once()
    mock_zip_instance.write.assert_called_once_with(mock_source, 'test.txt')


def test_zip_command_directory(mocker: MockerFixture):
    """Тест создания ZIP архива из директории"""
    mock_source = mocker.MagicMock(spec=Path)
    mock_source.exists.return_value = True
    mock_source.is_file.return_value = False
    mock_source.is_dir.return_value = True
    
    mock_file = mocker.MagicMock(spec=Path)
    mock_file.is_file.return_value = True
    mock_file.is_dir.return_value = False
    mock_file.relative_to.return_value = "file.txt"
    
    mock_dir = mocker.MagicMock(spec=Path)
    mock_dir.is_file.return_value = False
    mock_dir.is_dir.return_value = True
    mock_dir.relative_to.return_value = "empty_dir"
    
    mock_source.rglob.return_value = [mock_file, mock_dir]
    
    mock_archive = mocker.MagicMock(spec=Path)
    mock_archive.suffix = '.zip'
    
    mock_path_class = mocker.patch('src.paths.Path')
    mock_path_class.side_effect = [mock_source, mock_archive]
    
    mock_zipfile = mocker.patch('src.zip.zipfile.ZipFile')
    mock_zip_instance = mocker.MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
    
    zip_command("source_folder archive.zip")
    
    mock_source.exists.assert_called_once()
    mock_source.is_dir.assert_called_once()
    mock_zip_instance.write.assert_called_once_with(mock_file, "file.txt")
    mock_zip_instance.writestr.assert_called_once_with("empty_dir/", '')


def test_unzip_command_success(mocker: MockerFixture):
    """Тест успешной распаковки ZIP архива"""
    mock_archive = mocker.MagicMock(spec=Path)
    mock_archive.exists.return_value = True
    mock_archive.suffix = '.zip'
    
    mock_path_class = mocker.patch('src.paths.Path', return_value=mock_archive)
    
    mock_zipfile = mocker.patch('src.zip.zipfile.ZipFile')
    
    unzip_command("archive.zip")
    
    mock_archive.exists.assert_called_once()
    mock_zipfile.assert_called_once_with(mock_archive, 'r')


def test_unzip_command_nonexistent_archive():
    """Тест распаковки несуществующего ZIP архива"""
    with pytest.raises(ShellError):
        unzip_command("nonexistent.zip")


def test_tar_command_file(mocker: MockerFixture):
    """Тест создания TAR.GZ архива из файла"""
    mock_source = mocker.MagicMock(spec=Path)
    mock_source.exists.return_value = True
    mock_source.is_file.return_value = True
    mock_source.is_dir.return_value = False
    mock_source.name = 'test.txt'
    
    mock_archive = mocker.MagicMock(spec=Path)
    mock_archive.suffix = '.gz'
    mock_archive.name = 'archive.tar.gz'
    
    mock_path_class = mocker.patch('src.paths.Path')
    mock_path_class.side_effect = [mock_source, mock_archive]
    
    mock_tarfile = mocker.patch('src.tar.tarfile.open')
    mock_tar_instance = mocker.MagicMock()
    mock_tarfile.return_value.__enter__.return_value = mock_tar_instance
    
    tar_command("test.txt archive.tar.gz")
    
    mock_source.exists.assert_called_once()
    mock_tar_instance.add.assert_called_once_with(mock_source, arcname='test.txt')


def test_tar_command_directory(mocker: MockerFixture):
    """Тест создания TAR.GZ архива из директории"""
    mock_source = mocker.MagicMock(spec=Path)
    mock_source.exists.return_value = True
    mock_source.is_file.return_value = False
    mock_source.is_dir.return_value = True
    mock_source.name = 'source_folder'
    
    mock_archive = mocker.MagicMock(spec=Path)
    mock_archive.suffix = '.gz'
    mock_archive.name = 'archive.tar.gz'
    
    mock_path_class = mocker.patch('src.paths.Path')
    mock_path_class.side_effect = [mock_source, mock_archive]
    
    mock_tarfile = mocker.patch('src.tar.tarfile.open')
    mock_tar_instance = mocker.MagicMock()
    mock_tarfile.return_value.__enter__.return_value = mock_tar_instance
    
    tar_command("source_folder archive.tar.gz")
    
    mock_source.exists.assert_called_once()
    mock_tar_instance.add.assert_called_once_with(mock_source, arcname='source_folder')


def test_untar_command_success(mocker: MockerFixture):
    """Тест успешной распаковки TAR.GZ архива"""
    mock_archive = mocker.MagicMock(spec=Path)
    mock_archive.exists.return_value = True
    mock_archive.suffix = '.gz'
    mock_archive.name = 'archive.tar.gz'
    
    mock_tarfile = mocker.patch('src.tar.tarfile.open')
    mock_path_class = mocker.patch('src.paths.Path', return_value=mock_archive)
    
    untar_command("archive.tar.gz")
    
    mock_archive.exists.assert_called_once()
    mock_tarfile.assert_called_once_with(mock_archive, 'r:gz')