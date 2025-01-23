# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

# pylint: disable=redefined-outer-name

"""
Unit tests for the `qbraid_cli.files.app` module.

"""

from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from qbraid_cli.files.app import files_app


@pytest.fixture
def runner():
    """Fixture for invoking CLI commands."""
    return CliRunner()


def test_files_upload(runner, tmp_path):
    """Test the `files upload` command."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content")

    with patch("qbraid_core.services.files.FileManagerClient") as mock_client:
        mock_client.return_value.upload_file.return_value = {
            "namespace": "user",
            "objectPath": "test_file.txt",
        }

        result = runner.invoke(files_app, ["upload", str(test_file)])

    assert result.exit_code == 0
    assert "File uploaded successfully!" in result.stdout
    assert "Namespace: 'user'" in result.stdout
    assert "Object path: 'test_file.txt'" in result.stdout


def test_files_upload_with_options(runner, tmp_path):
    """Test the `files upload` command with options."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content")

    with patch("qbraid_core.services.files.FileManagerClient") as mock_client:
        mock_client.return_value.upload_file.return_value = {
            "namespace": "custom",
            "objectPath": "folder/test_file.txt",
        }

        result = runner.invoke(
            files_app,
            [
                "upload",
                str(test_file),
                "--namespace",
                "custom",
                "--object-path",
                "folder/test_file.txt",
                "--overwrite",
            ],
        )

    assert result.exit_code == 0
    assert "File uploaded successfully!" in result.stdout
    assert "Namespace: 'custom'" in result.stdout
    assert "Object path: 'folder/test_file.txt'" in result.stdout


def test_files_download(runner, tmp_path):
    """Test the `files download` command."""
    with patch("qbraid_core.services.files.FileManagerClient") as mock_client:
        mock_client.return_value.download_file.return_value = tmp_path / "downloaded_file.txt"

        result = runner.invoke(files_app, ["download", "test_file.txt"])

    assert result.exit_code == 0
    assert "File downloaded successfully!" in result.stdout
    assert f"Saved to: '{(tmp_path / 'downloaded_file.txt')}'" in result.stdout.replace("\n", "")


def test_files_download_with_options(runner, tmp_path):
    """Test the `files download` command with options."""
    save_path = tmp_path / "custom_folder"
    save_path.mkdir()

    with patch("qbraid_core.services.files.FileManagerClient") as mock_client:
        mock_client.return_value.download_file.return_value = save_path / "downloaded_file.txt"

        result = runner.invoke(
            files_app,
            [
                "download",
                "folder/test_file.txt",
                "--namespace",
                "custom",
                "--save-path",
                str(save_path),
                "--overwrite",
            ],
        )

    assert result.exit_code == 0
    assert "File downloaded successfully!" in result.stdout
    assert f"Saved to: '{(save_path / 'downloaded_file.txt')}'" in result.stdout.replace("\n", "")
