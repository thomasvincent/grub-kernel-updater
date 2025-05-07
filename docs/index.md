# Grub Kernel Updater Documentation

Welcome to the Grub Kernel Updater documentation. This utility helps you manage the default kernel version in your GRUB boot configuration.

## Contents

- [Usage Guide](usage.md): Instructions for using the tool
- [Architecture](architecture.md): Technical details about the design

## Quick Start

### Installation

```bash
# From GitHub
git clone https://github.com/thomasvincent/grub-kernel-updater.git
cd grub-kernel-updater
pip install -e .

# Using pip (once published)
pip install grub-kernel-updater
```

### Basic Usage

```bash
# Set highest kernel version as default
sudo grub-kernel-updater

# List available kernel versions
grub-kernel-updater --list-only

# Set specific version as default
sudo grub-kernel-updater --version 5.10.0-1234
```

## Key Features

- Automatically sets the highest available kernel version as default
- Supports manual selection of a specific kernel version
- Easy-to-use command line interface
- Python API for integration with other tools
- Robust error handling and validation

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.