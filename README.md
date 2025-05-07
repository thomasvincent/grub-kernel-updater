# Grub Kernel Updater

[![Python Tests](https://github.com/thomasvincent/grub-kernel-updater/actions/workflows/python-tests.yml/badge.svg)](https://github.com/thomasvincent/grub-kernel-updater/actions/workflows/python-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A Python utility for managing GRUB boot configuration by updating the default kernel version.

## Features

- Automatically sets the highest available kernel version as the default boot option
- Supports manual selection of a specific kernel version
- Easy-to-use command-line interface
- Robust error handling and validation
- Docker support for containerized execution

## Installation

### From GitHub

```bash
# Clone the repository
git clone https://github.com/thomasvincent/grub-kernel-updater.git
cd grub-kernel-updater

# Install the package
pip install -e .
```

### Using pip (once published to PyPI)

```bash
pip install grub-kernel-updater
```

### Using Docker

```bash
# Build the Docker image
docker build -t grub-kernel-updater .

# Run in list-only mode (non-destructive)
docker run -v /etc/grub.conf:/mnt/grub/grub.conf:ro grub-kernel-updater --list-only
```

See the [Docker documentation](docs/docker.md) for more details.

## Usage

### Command Line Interface

```bash
# Set the highest available kernel version as default
sudo grub-kernel-updater

# Use a custom GRUB configuration file path
sudo grub-kernel-updater --config /path/to/grub.conf

# List available kernel versions without making changes
grub-kernel-updater --list-only

# Set a specific kernel version as default
sudo grub-kernel-updater --version 5.10.0-1234
```

### As a Python Package

```python
from grub_kernel_updater.core import GrubConf, KernelManager

# Initialize with the path to the GRUB configuration file
grub_conf = GrubConf("/etc/grub.conf")

# Get available kernel versions
versions = grub_conf.get_kernel_versions()
print(f"Available kernel versions: {versions}")

# Set a specific kernel version as default
grub_conf.set_default_kernel("5.10.0-1234")

# Or automatically set the highest version as default
kernel_manager = KernelManager(grub_conf)
highest_version = kernel_manager.set_highest_kernel_as_default()
print(f"Set default kernel to: {highest_version}")
```

## Important Notes

- **Root Privileges**: You need root privileges to modify the GRUB configuration file
- **Backup**: Consider backing up your GRUB configuration before using this tool
- **Compatibility**: This tool assumes a specific format for GRUB configuration files - it may need adjustments for your system

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/thomasvincent/grub-kernel-updater.git
cd grub-kernel-updater

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Run Linters and Type Checking

```bash
flake8 grub_kernel_updater tests
black --check grub_kernel_updater tests
isort --check-only grub_kernel_updater tests
mypy grub_kernel_updater
```

### Docker Development

```bash
# Build the Docker image
docker build -t grub-kernel-updater .

# Run the tests in Docker
docker run -it --rm grub-kernel-updater pytest
```

## Documentation

- [Usage Guide](docs/usage.md) - Detailed usage instructions
- [Architecture](docs/architecture.md) - Technical architecture and design
- [Docker Guide](docs/docker.md) - Docker usage instructions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.