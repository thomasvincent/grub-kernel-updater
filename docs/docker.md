# Docker Support for Grub Kernel Updater

This document explains how to run the Grub Kernel Updater using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for using docker-compose.yml)

## Quick Start

### Using Docker Run

```bash
# Build the Docker image
docker build -t grub-kernel-updater .

# Run in list-only mode (non-destructive)
docker run -v /etc/grub.conf:/mnt/grub/grub.conf:ro grub-kernel-updater --config /mnt/grub/grub.conf --list-only

# Run to set the highest kernel version as default (requires write access)
docker run -v /etc/grub.conf:/mnt/grub/grub.conf:rw grub-kernel-updater --config /mnt/grub/grub.conf
```

### Using Docker Compose

```bash
# Set the path to your GRUB configuration
export GRUB_CONFIG_PATH=/etc/grub.conf

# Run in list-only mode (modify docker-compose.yml to add --list-only flag)
docker-compose up

# Run once and remove the container
docker-compose up --rm
```

## Configuration Options

### Mount Points

The Docker container expects the GRUB configuration file to be mounted at `/mnt/grub/grub.conf`. Adjust your volume mount accordingly if your GRUB configuration is at a different location.

### Command Arguments

The Docker container accepts the same command-line arguments as the normal application:

- `--config PATH`: Path to the GRUB configuration file (default: /mnt/grub/grub.conf in Docker)
- `--list-only`: Only list available kernel versions without making changes
- `--version VERSION`: Specify a kernel version to set as default

## Security Considerations

### Running with Least Privilege

The Docker container runs as a non-root user `appuser` to enhance security. However, it still needs write access to the GRUB configuration file to make changes.

### Read-Only Mode

If you only want to list available kernel versions without making changes, mount the GRUB configuration as read-only:

```bash
docker run -v /etc/grub.conf:/mnt/grub/grub.conf:ro grub-kernel-updater --config /mnt/grub/grub.conf --list-only
```

## Examples

### Listing Available Kernel Versions

```bash
docker run -v /etc/grub.conf:/mnt/grub/grub.conf:ro grub-kernel-updater --config /mnt/grub/grub.conf --list-only
```

### Setting a Specific Kernel Version as Default

```bash
docker run -v /etc/grub.conf:/mnt/grub/grub.conf:rw grub-kernel-updater --config /mnt/grub/grub.conf --version 5.10.0-1234
```

### Custom GRUB Configuration Path

```bash
docker run -v /path/to/custom/grub.conf:/mnt/grub/custom.conf:rw grub-kernel-updater --config /mnt/grub/custom.conf
```

## Building a Custom Image

You can build a custom Docker image with specific settings:

```dockerfile
FROM grub-kernel-updater:latest

# Set custom default command
CMD ["--config", "/mnt/grub/grub.conf", "--list-only"]
```

Then build and run the custom image:

```bash
docker build -t my-grub-updater -f CustomDockerfile .
docker run -v /etc/grub.conf:/mnt/grub/grub.conf:ro my-grub-updater
```