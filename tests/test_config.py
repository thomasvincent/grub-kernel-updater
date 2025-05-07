"""Tests for the config module."""

import os
import tempfile
import pytest

from grub_kernel_updater.config import (
    FileSystemConfigReader,
    KernelVersionExtractor,
    KernelVersionSelector,
)


@pytest.fixture
def config_file():
    """Create a temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(b"kernel /boot/vmlinuz-5.10.0-1234\n")
        file.write(b"kernel /boot/vmlinuz-5.11.0-5678\n")
        file.write(b"some other content\n")
        file.flush()
        yield file.name
        os.unlink(file.name)


def test_filesystem_config_reader(config_file):
    """Test FileSystemConfigReader."""
    reader = FileSystemConfigReader()
    content = reader.read_file(config_file)
    
    assert "kernel /boot/vmlinuz-5.10.0-1234" in content
    assert "kernel /boot/vmlinuz-5.11.0-5678" in content
    assert "some other content" in content


def test_filesystem_config_reader_file_not_found():
    """Test FileSystemConfigReader with non-existent file."""
    reader = FileSystemConfigReader()
    with pytest.raises(FileNotFoundError):
        reader.read_file("/path/does/not/exist")


def test_kernel_version_extractor():
    """Test KernelVersionExtractor."""
    extractor = KernelVersionExtractor()
    content = """
    kernel /boot/vmlinuz-5.10.0-1234
    kernel /boot/vmlinuz-5.11.0-5678
    some other content
    """
    versions = extractor.extract_versions(content)
    
    assert versions == ["5.10.0-1234", "5.11.0-5678"]


def test_kernel_version_extractor_custom_pattern():
    """Test KernelVersionExtractor with custom pattern."""
    import re
    extractor = KernelVersionExtractor(re.compile(r"vmlinuz-([\d.]+-\d+)"))
    content = """
    vmlinuz-5.10.0-1234
    vmlinuz-5.11.0-5678
    some other content
    """
    versions = extractor.extract_versions(content)
    
    assert versions == ["5.10.0-1234", "5.11.0-5678"]


def test_kernel_version_extractor_no_matches():
    """Test KernelVersionExtractor with no matches."""
    extractor = KernelVersionExtractor()
    content = """
    no kernel versions here
    just some other content
    """
    versions = extractor.extract_versions(content)
    
    assert versions == []


def test_kernel_version_selector_highest():
    """Test KernelVersionSelector.select_highest_version."""
    versions = ["5.10.0-1234", "5.11.0-5678", "5.9.0-4321"]
    highest = KernelVersionSelector.select_highest_version(versions)
    
    assert highest == "5.11.0-5678"


def test_kernel_version_selector_empty():
    """Test KernelVersionSelector.select_highest_version with empty list."""
    highest = KernelVersionSelector.select_highest_version([])
    
    assert highest is None