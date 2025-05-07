"""Tests for the modifier module."""

import pytest
import subprocess
from unittest.mock import MagicMock, patch

from grub_kernel_updater.modifier import (
    ConfigModifier,
    DefaultKernelModifier,
    SedConfigModifier,
)


def test_sed_config_modifier():
    """Test SedConfigModifier."""
    # Mock subprocess.run
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        
        # Create SedConfigModifier
        modifier = SedConfigModifier()
        
        # Test modify_config
        modifier.modify_config("/mock/path", "s/old/new/")
        
        # Verify subprocess.run was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        command = args[0]
        assert command[0] == "/usr/bin/sed"
        assert command[2] == "s/old/new/"
        assert command[3] == "/mock/path"
        assert kwargs["check"] is True


def test_sed_config_modifier_custom_path():
    """Test SedConfigModifier with custom sed path."""
    # Mock subprocess.run
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        
        # Create SedConfigModifier with custom sed path
        modifier = SedConfigModifier("/custom/sed")
        
        # Test modify_config
        modifier.modify_config("/mock/path", "s/old/new/")
        
        # Verify subprocess.run was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        command = args[0]
        assert command[0] == "/custom/sed"


def test_sed_config_modifier_error():
    """Test SedConfigModifier error handling."""
    # Mock subprocess.run to raise CalledProcessError
    error = subprocess.CalledProcessError(1, "sed")
    error.stderr = "Some error message"
    
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = error
        
        # Create SedConfigModifier
        modifier = SedConfigModifier()
        
        # Test modify_config
        with pytest.raises(RuntimeError):
            modifier.modify_config("/mock/path", "s/old/new/")


def test_default_kernel_modifier():
    """Test DefaultKernelModifier."""
    # Mock ConfigModifier
    mock_modifier = MagicMock(spec=ConfigModifier)
    
    # Create DefaultKernelModifier
    default_modifier = DefaultKernelModifier(mock_modifier)
    
    # Test set_default_kernel
    default_modifier.set_default_kernel("/mock/path", "5.11.0-5678")
    
    # Verify ConfigModifier.modify_config was called correctly
    mock_modifier.modify_config.assert_called_once()
    args, kwargs = mock_modifier.modify_config.call_args
    assert args[0] == "/mock/path"
    assert args[1] == "s/default=.*/default=5.11.0-5678/"