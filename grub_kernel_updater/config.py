"""Configuration handling for Grub Kernel Updater."""

import os
import re
from abc import ABC, abstractmethod
from functools import cmp_to_key
from typing import List, Optional, Pattern


class ConfigReader(ABC):
    """Abstract base class for configuration readers."""

    @abstractmethod
    def read_file(self, path: str) -> str:
        """Read the content of a file.
        
        Args:
            path: Path to the file to read
            
        Returns:
            Content of the file
            
        Raises:
            FileNotFoundError: If the file does not exist
        """
        pass


class FileSystemConfigReader(ConfigReader):
    """File system based configuration reader."""

    def read_file(self, path: str) -> str:
        """Read the content of a file from the filesystem.
        
        Args:
            path: Path to the file to read
            
        Returns:
            Content of the file
            
        Raises:
            FileNotFoundError: If the file does not exist
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File does not exist at {path}")
        
        with open(path, encoding="utf-8") as file:
            return file.read()


class KernelVersionExtractor:
    """Extracts kernel versions from configuration content."""

    def __init__(self, pattern: Optional[Pattern] = None):
        """Initialize with an optional regex pattern.
        
        Args:
            pattern: Regex pattern to use for extracting kernel versions
        """
        self.pattern = pattern or re.compile(r"kernel\s+/boot/vmlinuz-([\d.]+-\d+)")

    def extract_versions(self, content: str) -> List[str]:
        """Extract kernel versions from the given content.
        
        Args:
            content: Content to extract versions from
            
        Returns:
            List of kernel versions found in the content
        """
        return [match.group(1) for match in self.pattern.finditer(content) if match.group(1)]


class KernelVersionSelector:
    """Selects kernel versions based on different strategies."""

    @staticmethod
    def _compare_versions(v1: str, v2: str) -> int:
        """Compare two kernel versions.
        
        Args:
            v1: First version to compare
            v2: Second version to compare
            
        Returns:
            -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2
        """
        # Split into components
        v1_base, v1_extra = v1.split("-", 1) if "-" in v1 else (v1, "0")
        v2_base, v2_extra = v2.split("-", 1) if "-" in v2 else (v2, "0")
        
        # Compare base versions
        v1_parts = [int(part) for part in v1_base.split(".")]
        v2_parts = [int(part) for part in v2_base.split(".")]
        
        # Extend shorter version with zeroes
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        # Compare part by part
        for i in range(max_len):
            if v1_parts[i] != v2_parts[i]:
                return 1 if v1_parts[i] > v2_parts[i] else -1
        
        # If base versions are the same, compare extra parts
        try:
            v1_extra_int = int(v1_extra)
            v2_extra_int = int(v2_extra)
            return 1 if v1_extra_int > v2_extra_int else (-1 if v1_extra_int < v2_extra_int else 0)
        except ValueError:
            # If extras can't be converted to int, compare as strings
            return 1 if v1_extra > v2_extra else (-1 if v1_extra < v2_extra else 0)

    @classmethod
    def select_highest_version(cls, versions: List[str]) -> Optional[str]:
        """Select the highest kernel version from the given list.
        
        Args:
            versions: List of kernel versions
            
        Returns:
            The highest kernel version, or None if the list is empty
        """
        if not versions:
            return None
            
        return max(versions, key=cmp_to_key(cls._compare_versions))