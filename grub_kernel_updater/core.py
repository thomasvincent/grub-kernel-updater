"""Core functionality for managing GRUB configuration."""

import os
from typing import List, Optional

from grub_kernel_updater.config import (
    ConfigReader,
    FileSystemConfigReader,
    KernelVersionExtractor,
    KernelVersionSelector,
)
from grub_kernel_updater.modifier import ConfigModifier, DefaultKernelModifier, SedConfigModifier


class GrubConf:
    """Handles operations related to the GRUB configuration file."""

    def __init__(
        self, 
        path: str,
        config_reader: Optional[ConfigReader] = None,
        version_extractor: Optional[KernelVersionExtractor] = None,
        config_modifier: Optional[ConfigModifier] = None
    ):
        """Initialize with the path to the GRUB configuration file.
        
        Args:
            path: Path to the GRUB configuration file
            config_reader: ConfigReader to use for reading the file
            version_extractor: KernelVersionExtractor to use for extracting versions
            config_modifier: ConfigModifier to use for modifying the file
            
        Raises:
            FileNotFoundError: If the GRUB configuration file does not exist
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"GRUB configuration file does not exist at {path}")
        
        self.path = path
        self.config_reader = config_reader or FileSystemConfigReader()
        self.version_extractor = version_extractor or KernelVersionExtractor()
        self.default_modifier = DefaultKernelModifier(
            config_modifier or SedConfigModifier()
        )

    def get_kernel_versions(self) -> List[str]:
        """Extract kernel versions from the configuration file.
        
        Returns:
            List of kernel versions found in the configuration file
        """
        content = self.config_reader.read_file(self.path)
        return self.version_extractor.extract_versions(content)

    def set_default_kernel(self, version: str) -> None:
        """Set the specified kernel version as default in the configuration file.
        
        Args:
            version: Kernel version to set as default
            
        Raises:
            RuntimeError: If updating the GRUB configuration fails
        """
        self.default_modifier.set_default_kernel(self.path, version)


class KernelManager:
    """Manages kernel versions for the application."""

    def __init__(self, grub_conf: GrubConf):
        """Initialize with a GrubConf instance.
        
        Args:
            grub_conf: Instance of GrubConf to use for kernel management
        """
        self.grub_conf = grub_conf

    def set_highest_kernel_as_default(self) -> Optional[str]:
        """Set the highest kernel version as the default one.
        
        Returns:
            The highest kernel version if successful, None otherwise
        """
        versions = self.grub_conf.get_kernel_versions()
        if not versions:
            return None

        highest_version = KernelVersionSelector.select_highest_version(versions)
        if highest_version:
            self.grub_conf.set_default_kernel(highest_version)
        
        return highest_version