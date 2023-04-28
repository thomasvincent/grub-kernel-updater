import os
import tempfile
import pytest
from contextlib import redirect_stdout
from io import StringIO
from app import GrubConf, App


@pytest.fixture
def grub_conf_file(request):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"kernel /boot/vmlinuz-5.10.0-1234\nkernel /boot/vmlinuz-5.11.0-5678\n")
        f.flush()
        yield f.name
        os.unlink(f.name)


def test_get_kernel_versions(grub_conf_file):
    versions = GrubConf(grub_conf_file).get_kernel_versions()
    assert versions == ["5.10.0-1234", "5.11.0-5678"]


def test_set_default_kernel_version(grub_conf_file):
    GrubConf(grub_conf_file).set_default_kernel_version("5.11.0-5678")

    # Verify that the default kernel was set correctly
    with open(grub_conf_file) as f:
        lines = f.readlines()
        assert any("default=0" in line for line in lines)
        assert any("kernel /boot/vmlinuz-5.11.0-5678" in line for line in lines)


@pytest.fixture
def app(grub_conf_file):
    yield App(grub_conf_file)


def test_app_run(capsys, app):
    app.run()

    # Verify that the output is correct
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    # Verify that the default kernel was set correctly
    with open(app.conf.path) as f:
        lines = f.readlines()
        assert any("default=0" in line for line in lines)
        assert any("kernel /boot/vmlinuz-5.11.0-5678" in line for line in lines)
