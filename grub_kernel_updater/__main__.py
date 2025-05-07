"""Entry point for the Grub Kernel Updater package."""

import sys
from grub_kernel_updater.cli import main

if __name__ == "__main__":
    sys.exit(main())