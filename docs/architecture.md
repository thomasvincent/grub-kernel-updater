# Grub Kernel Updater Architecture

This document explains the architecture of the Grub Kernel Updater, designed following SOLID principles.

## Overview

The Grub Kernel Updater is architected as a modular system with clear separation of concerns. The codebase follows:

- **Single Responsibility Principle**: Each class has a single responsibility
- **Open/Closed Principle**: Components are open for extension but closed for modification
- **Liskov Substitution Principle**: Derived classes can substitute base classes
- **Interface Segregation Principle**: Specific interfaces are better than general ones
- **Dependency Inversion Principle**: High-level modules depend on abstractions

## Component Structure

![Component Structure](https://mermaid.ink/img/pako:eNp1kk9PwzAMxb9KlBOgSfuKHjhAJSSOHOAUTcRLo9KkclxAVffdcdrCWAc-Jfa8_5zY47K3XlPJqk2dDRJXs9VV_RLKmZdvhEyQQTvDrxNhNiMSgGAfG-1qcZgA9KN74bpG-BihbsBvN59uYx0kYcuwgB0lPVm01LNJPN9PjFAH2kMg5yD4VNlEzRi3hNoESbZx3GiTVcUf5sNOYW8EZ0JZmG1rgzAPm0g3NCgkw7bJeXkX_Z1vHCOGCn6TJFGpDfQYxcJGiQSzFMWUa2-n-5Tj-uDSAF6CpWAC3QNz2Jnk-SXkT4Y0_sSJnUqsQm47nQQRmAi5Zft-GvKWaOi72AQzUr1ZxB6n00jlbxFZljn29TGm-5HGuMwzjnGZZzbjmD9-NKL-Y0RzBueYxr-iHw2LPfaIrGR9EVZV8h2U1KjEZpR5ydYuRNeJkoKrXmSPobLcQVnOH9FZvnFO-ge48_U4)

### Core Components

1. **GrubConf** (core.py)
   - Main class for interacting with GRUB configuration
   - Delegates to specialized components
   - Provides a high-level API for the CLI

2. **KernelManager** (core.py)
   - Handles operations related to kernel versions
   - Uses GrubConf to read and modify configuration
   - Provides business logic for kernel operations

### Configuration Components (config.py)

1. **ConfigReader** (Abstract)
   - Defines interface for reading configuration
   - Allows for different implementation strategies

2. **FileSystemConfigReader**
   - Concrete implementation of ConfigReader
   - Reads configuration from the file system

3. **KernelVersionExtractor**
   - Extracts kernel versions from configuration content
   - Uses regex patterns for version extraction
   - Can be customized with different patterns

4. **KernelVersionSelector**
   - Contains strategies for selecting kernel versions
   - Currently supports selecting highest version
   - Can be extended with additional strategies

### Modification Components (modifier.py)

1. **ConfigModifier** (Abstract)
   - Defines interface for modifying configuration
   - Allows for different implementation strategies

2. **SedConfigModifier**
   - Concrete implementation of ConfigModifier
   - Uses the 'sed' command to modify configuration files

3. **DefaultKernelModifier**
   - Specialized modifier for setting default kernel
   - Uses a ConfigModifier for the actual modification
   - Formats the modification command appropriately

### CLI Component (cli.py)

1. **Command Line Interface**
   - Handles parsing command-line arguments
   - Creates and uses core components
   - Provides user-friendly output
   - Returns appropriate exit codes

## Dependency Injection

A key feature of the architecture is the use of dependency injection:

```python
# Create with defaults
grub_conf = GrubConf("/etc/grub.conf")

# Or inject dependencies
grub_conf = GrubConf(
    "/etc/grub.conf",
    config_reader=custom_reader,
    version_extractor=custom_extractor,
    config_modifier=custom_modifier
)
```

This allows for:
- Easy testing with mock objects
- Customization of behavior without modifying code
- Extension with new implementations
- Adherence to SOLID principles

## Flow of Operation

1. CLI parses arguments
2. GrubConf is created with appropriate dependencies
3. ConfigReader reads the configuration file
4. KernelVersionExtractor extracts versions from content
5. KernelVersionSelector selects appropriate version
6. DefaultKernelModifier formats the modification
7. ConfigModifier applies the change to the file

This clear separation of concerns makes the code:
- Easier to understand
- Easier to maintain
- Easier to extend
- Easier to test