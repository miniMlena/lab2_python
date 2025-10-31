from pathlib import Path
from unittest.mock import Mock
import pytest
from src.errors import ShellError
from src.ls import ls

def test_ls_called_for_nonexisted_folder(mocker):
        fake_path_object: Mock = mocker.create_autospec(Path, instance=True, spec_set=True)
        fake_path_object.exists.return_value = False
        nonexistent_path: str = "/nonexistent"
        fake_path_class = mocker.patch('src.ls.Path', return_value=fake_path_object)

        with pytest.raises(ShellError):
                ls(nonexistent_path)

        fake_path_class.assert_called_with(nonexistent_path)
        fake_path_object.exists.assert_called_once()