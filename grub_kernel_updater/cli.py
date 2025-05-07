"""Command-line interface for the Grub Kernel Updater."""

import argparse
import sys
from typing import List, Optional

from grub_kernel_updater.core import GrubConf, KernelManager


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: Command-line arguments to parse. Defaults to sys.argv if None.
        
    Returns:
        Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Update the default kernel in GRUB configuration"
    )
    parser.add_argument(
        "--config", 
        default="/etc/grub.conf",
        help="Path to the GRUB configuration file (default: /etc/grub.conf)"
    )
    parser.add_argument(
        "--list-only", 
        action="store_true",
        help="Only list available kernel versions without making changes"
    )
    parser.add_argument(
        "--version", 
        help="Specify a kernel version to set as default (defaults to highest available)"
    )
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the command-line interface.
    
    Args:
        args: Command-line arguments. Defaults to sys.argv if None.
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parsed_args = parse_args(args)
    
    try:
        grub_conf = GrubConf(parsed_args.config)
        
        # List available kernel versions
        versions = grub_conf.get_kernel_versions()
        if not versions:
            print("No kernel versions found in GRUB configuration.")
            return 1
            
        print("Available kernel versions:")
        for version in versions:
            print(f"  - {version}")
            
        # Exit if only listing versions
        if parsed_args.list_only:
            return 0
            
        # Set specified version or highest as default
        kernel_manager = KernelManager(grub_conf)
        if parsed_args.version:
            if parsed_args.version not in versions:
                print(f"Error: Kernel version {parsed_args.version} not found in GRUB configuration.")
                return 1
            grub_conf.set_default_kernel(parsed_args.version)
            print(f"Successfully set default kernel to {parsed_args.version}.")
        else:
            highest_version = kernel_manager.set_highest_kernel_as_default()
            if highest_version:
                print(f"Successfully set default kernel to {highest_version} (highest available).")
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