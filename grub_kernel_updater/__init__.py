"""Grub Kernel Updater package.

A utility for managing GRUB boot configuration by updating the default kernel version.

Components:
    - core: Main functionality for managing GRUB configuration
    - config: Configuration reading and kernel version extraction
    - modifier: Configuration modification classes
    - cli: Command-line interface
"""

__version__ = "0.1.0"
__author__ = "Thomas Vincent"
__email__ = "thomasvincent@gmx.com"
__license__ = "MIT"
__copyright__ = "Copyright 2018-2024 Thomas Vincent"

from grub_kernel_updater.core import GrubConf, KernelManager