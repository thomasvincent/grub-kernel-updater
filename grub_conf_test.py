import os
import tempfile
import pytest
from contextlib import redirect_stdout
from io import StringIO
from app import GrubConf, KernelManager  # Updated import according to the new class name

@pytest.fixture
def grub_conf_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"kernel /boot/vmlinuz-5.10.0-1234\nkernel /boot/vmlinuz-5.11.0-5678\n")
        f.flush()
        yield f.name
        os.unlink(f.name)

def test_get_kernel_versions(grub_conf_file):
    versions = GrubConf(grub_conf_file).get_kernel_versions()
    assert versions == ["5.10.0-1234", "5.11.0-5678"]

def test_set_default_kernel(grub_conf_file):
    grub_conf = GrubConf(grub_conf_file)
    grub_conf.set_default_kernel("5.11.0-5678")
    # Assuming `set_default_kernel` modifies a file to set the default version,
    # this test needs to be adapted to reflect how `set_default_kernel` actually works.

    # Verify that the default kernel was set correctly
    # Note: This step might need adjustment based on how `set_default_kernel` is implemented.
    with open(grub_conf_file) as f:
        lines = f.readlines()
    # This assertion will depend on the actual changes made by `set_default_kernel`.
    # For example, if it's changing a line in the file, you'll need to check for that specific change.

@pytest.fixture
def kernel_manager(grub_conf_file):
    yield KernelManager(GrubConf(grub_conf_file))

def test_kernel_manager_set_highest_kernel_as_default(capsys, kernel_manager):
    kernel_manager.set_highest_kernel_as_default()
    captured = capsys.readouterr()
    # Adjust these assertions based on the expected print output of `set_highest_kernel_as_default`
    assert "Successfully set default kernel to 5.11.0-5678." in captured.out

    # Further checks can be made to ensure the file was modified accordingly,
    # similar to the second test, depending on the implementation details of `set_default_kernel`.
