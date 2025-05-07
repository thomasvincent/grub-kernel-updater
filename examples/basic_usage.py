#!/usr/bin/env python3
"""
Example script demonstrating basic usage of the Grub Kernel Updater.

This script shows how to use the Grub Kernel Updater as a Python library.
"""

import sys
from grub_kernel_updater.core import GrubConf, KernelManager


def main():
    """Demonstrate basic usage of the Grub Kernel Updater."""
    # Replace with your actual GRUB configuration path
    grub_path = "/etc/grub.conf"
    
    try:
        # Initialize GrubConf with the configuration path
        grub_conf = GrubConf(grub_path)
        
        # Get available kernel versions
        versions = grub_conf.get_kernel_versions()
        print(f"Available kernel versions ({len(versions)}):")
        for version in versions:
            print(f"  - {version}")
        
        if not versions:
            print("No kernel versions found.")
            return 1
        
        # Create a KernelManager
        kernel_manager = KernelManager(grub_conf)
        
        # Set the highest kernel version as default
        highest_version = kernel_manager.set_highest_kernel_as_default()
        if highest_version:
            print(f"Successfully set default kernel to {highest_version}.")
        else:
            print("Failed to set default kernel.")
            return 1
        
        return 0
    
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return 1
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())