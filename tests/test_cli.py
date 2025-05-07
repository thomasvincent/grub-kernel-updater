"""Tests for the command-line interface."""

import os
import tempfile
import pytest
from unittest.mock import patch

from grub_kernel_updater.cli import main, parse_args


@pytest.fixture
def grub_conf_file():
    """Create a temporary GRUB configuration file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(b"default=5.10.0-1234\n")
        file.write(b"kernel /boot/vmlinuz-5.10.0-1234\n")
        file.write(b"kernel /boot/vmlinuz-5.11.0-5678\n")
        file.flush()
        yield file.name
        os.unlink(file.name)


def test_parse_args_defaults():
    """Test parsing command-line arguments with defaults."""
    args = parse_args([])
    assert args.config == "/etc/grub.conf"
    assert not args.list_only
    assert args.version is None


def test_parse_args_custom():
    """Test parsing command-line arguments with custom values."""
    args = parse_args(["--config", "/custom/path", "--list-only", "--version", "5.10.0"])
    assert args.config == "/custom/path"
    assert args.list_only
    assert args.version == "5.10.0"


def test_main_list_only(grub_conf_file, capsys):
    """Test listing kernel versions without making changes."""
    exit_code = main(["--config", grub_conf_file, "--list-only"])
    
    captured = capsys.readouterr()
    assert "Available kernel versions:" in captured.out
    assert "5.10.0-1234" in captured.out
    assert "5.11.0-5678" in captured.out
    assert exit_code == 0


def test_main_set_specific_version(grub_conf_file, capsys):
    """Test setting a specific kernel version as default."""
    with patch("grub_kernel_updater.core.GrubConf.set_default_kernel") as mock_set_default:
        exit_code = main(["--config", grub_conf_file, "--version", "5.10.0-1234"])
        
        captured = capsys.readouterr()
        assert "Successfully set default kernel to 5.10.0-1234" in captured.out
        mock_set_default.assert_called_once_with("5.10.0-1234")
        assert exit_code == 0


def test_main_set_highest_version(grub_conf_file, capsys):
    """Test setting the highest kernel version as default."""
    with patch("grub_kernel_updater.core.KernelManager.set_highest_kernel_as_default", 
               return_value="5.11.0-5678") as mock_set_highest:
        exit_code = main(["--config", grub_conf_file])
        
        captured = capsys.readouterr()
        assert "Successfully set default kernel to 5.11.0-5678" in captured.out
        assert "(highest available)" in captured.out
        mock_set_highest.assert_called_once()
        assert exit_code == 0


def test_main_invalid_version(grub_conf_file, capsys):
    """Test error handling for invalid kernel version."""
    exit_code = main(["--config", grub_conf_file, "--version", "999.999.999"])
    
    captured = capsys.readouterr()
    assert "Error: Kernel version 999.999.999 not found" in captured.out
    assert exit_code == 1


def test_main_no_versions(grub_conf_file, capsys):
    """Test handling when no kernel versions are found."""
    with patch("grub_kernel_updater.core.GrubConf.get_kernel_versions", return_value=[]):
        exit_code = main(["--config", grub_conf_file])
        
        captured = capsys.readouterr()
        assert "No kernel versions found" in captured.out
        assert exit_code == 1