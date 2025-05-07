"""Configuration modifiers for Grub Kernel Updater."""

import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional


class ConfigModifier(ABC):
    """Abstract base class for configuration modifiers."""

    @abstractmethod
    def modify_config(self, path: str, modification: str) -> None:
        """Modify a configuration file.
        
        Args:
            path: Path to the configuration file
            modification: Modification to apply
            
        Raises:
            RuntimeError: If the modification fails
        """
        pass


class SedConfigModifier(ConfigModifier):
    """Configuration modifier using sed."""

    def __init__(self, sed_path: str = "/usr/bin/sed"):
        """Initialize with the path to the sed binary.
        
        Args:
            sed_path: Path to the sed binary
        """
        self.sed_path = sed_path

    def modify_config(self, path: str, modification: str) -> None:
        """Modify a configuration file using sed.
        
        Args:
            path: Path to the configuration file
            modification: Modification to apply (the sed pattern)
            
        Raises:
            RuntimeError: If the modification fails
        """
        sed_command = [self.sed_path, "-i.bak", modification, path]
        try:
            result = subprocess.run(
                sed_command, 
                check=True, 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"Sed command failed: {result.stderr}")
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"Failed to update the configuration: {exc.stderr}") from exc


class DefaultKernelModifier:
    """Modifier for setting the default kernel in GRUB configuration."""

    def __init__(self, config_modifier: ConfigModifier):
        """Initialize with a ConfigModifier.
        
        Args:
            config_modifier: The ConfigModifier to use
        """
        self.config_modifier = config_modifier

    def set_default_kernel(self, config_path: str, kernel_version: str) -> None:
        """Set the default kernel version in the configuration.
        
        Args:
            config_path: Path to the configuration file
            kernel_version: Kernel version to set as default
            
        Raises:
            RuntimeError: If the modification fails
        """
        modification = f"s/default=.*/default={kernel_version}/"
        self.config_modifier.modify_config(config_path, modification)