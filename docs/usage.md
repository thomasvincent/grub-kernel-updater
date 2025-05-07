# Grub Kernel Updater Usage Guide

This document provides comprehensive usage instructions for the Grub Kernel Updater.

## Basic Usage

The Grub Kernel Updater is primarily used as a command-line tool. Here are the basic usage patterns:

### Setting the Highest Kernel Version as Default

```bash
sudo grub-kernel-updater
```

This will:
1. Scan your GRUB configuration file (`/etc/grub.conf` by default)
2. Find all available kernel versions
3. Determine the highest version
4. Set that version as the default boot option
5. Report the results

### Listing Available Kernel Versions

If you just want to see what kernel versions are available without making any changes:

```bash
grub-kernel-updater --list-only
```

### Specifying a Different GRUB Configuration File

If your GRUB configuration is in a non-standard location:

```bash
sudo grub-kernel-updater --config /path/to/your/grub.conf
```

### Setting a Specific Kernel Version as Default

If you want to select a specific version rather than automatically using the highest:

```bash
sudo grub-kernel-updater --version 5.10.0-1234
```

Note: The specified version must exist in your GRUB configuration.

## Advanced Usage

### Using the Python API

The Grub Kernel Updater can also be used as a Python library in your own scripts:

```python
from grub_kernel_updater.core import GrubConf, KernelManager

# Initialize with the path to your GRUB configuration
grub_conf = GrubConf("/etc/grub.conf")

# Get all available kernel versions
versions = grub_conf.get_kernel_versions()
print(f"Available kernel versions: {versions}")

# Set a specific version as default
grub_conf.set_default_kernel("5.10.0-1234")

# Or automatically set the highest version
kernel_manager = KernelManager(grub_conf)
highest_version = kernel_manager.set_highest_kernel_as_default()
print(f"Set highest kernel version as default: {highest_version}")
```

### Dependency Injection

The library supports dependency injection, allowing you to customize its behavior:

```python
import re
from grub_kernel_updater.core import GrubConf
from grub_kernel_updater.config import FileSystemConfigReader, KernelVersionExtractor
from grub_kernel_updater.modifier import SedConfigModifier

# Custom configuration reader
custom_reader = FileSystemConfigReader()

# Custom version extractor with a different pattern
custom_extractor = KernelVersionExtractor(re.compile(r"custom-kernel-([\d.]+)"))

# Custom modifier with a different sed path
custom_modifier = SedConfigModifier("/usr/local/bin/sed")

# Create GrubConf with custom components
grub_conf = GrubConf(
    "/etc/grub.conf",
    config_reader=custom_reader,
    version_extractor=custom_extractor,
    config_modifier=custom_modifier
)

# Use GrubConf as normal
versions = grub_conf.get_kernel_versions()
```

## Troubleshooting

### Permission Issues

If you encounter permission issues, ensure you're running the command with `sudo` when it needs to modify the GRUB configuration file.

### No Kernel Versions Found

If the tool reports that no kernel versions were found:

1. Check that your GRUB configuration file exists at the expected location
2. Verify that the file contains kernel entries in the expected format
3. Consider using a custom pattern with the `KernelVersionExtractor` if your configuration uses a different format

### Failed to Update GRUB Configuration

If the tool fails to update the GRUB configuration:

1. Ensure the `sed` command is available at `/usr/bin/sed` (or specify a custom path)
2. Check that the GRUB configuration file is writable
3. Verify that the file contains a `default=` line that can be modified