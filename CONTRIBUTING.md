# Contributing to Grub Kernel Updater

Thank you for your interest in contributing to the Grub Kernel Updater project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct: be respectful, considerate, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue in the GitHub repository with the following information:

1. A clear, descriptive title
2. A detailed description of the issue
3. Steps to reproduce the bug
4. Expected behavior
5. Actual behavior
6. Your environment (OS, Python version, etc.)

### Suggesting Enhancements

If you have an idea for an enhancement, please create an issue with:

1. A clear, descriptive title
2. A detailed description of the enhancement
3. The motivation behind it
4. Possible implementation approaches (if you have ideas)

### Pull Requests

We welcome pull requests for bug fixes, enhancements, or new features. Here's how to submit a pull request:

1. Fork the repository
2. Create a branch for your changes (`git checkout -b feature/my-new-feature`)
3. Make your changes
4. Run tests to ensure they pass (`pytest`)
5. Run linting to ensure code quality (`flake8`, `black`, `isort`, `mypy`)
6. Commit your changes (`git commit -am 'Add some feature'`)
7. Push to the branch (`git push origin feature/my-new-feature`)
8. Create a Pull Request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/thomasvincent/grub-kernel-updater.git
   cd grub-kernel-updater
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

5. Run linting and type checking:
   ```bash
   flake8 grub_kernel_updater tests
   black --check grub_kernel_updater tests
   isort --check --profile black grub_kernel_updater tests
   mypy grub_kernel_updater
   ```

## Style Guide

### Python Code Style

- Follow PEP 8 guidelines
- Use Black for formatting
- Use isort for import sorting
- Use type hints for function parameters and return values
- Write docstrings for all modules, classes, and functions

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in the present tense (e.g., "Add feature" not "Added feature")
- Keep the first line under 50 characters
- Provide more details in the commit body if needed

## Project Structure

```
grub-kernel-updater/
├── docs/                 # Documentation
├── grub_kernel_updater/  # Main package
│   ├── __init__.py       # Package initialization
│   ├── __main__.py       # Entry point
│   ├── cli.py            # Command-line interface
│   ├── config.py         # Configuration components
│   ├── core.py           # Core functionality
│   └── modifier.py       # Configuration modifiers
├── tests/                # Test package
│   ├── __init__.py       # Test package initialization
│   ├── test_cli.py       # CLI tests
│   ├── test_config.py    # Configuration tests
│   ├── test_core.py      # Core tests
│   └── test_modifier.py  # Modifier tests
├── .github/              # GitHub configuration
├── LICENSE               # Project license
├── pyproject.toml        # Project configuration
├── README.md             # Project overview
├── requirements.txt      # Dependencies
├── setup.py              # Package setup
└── tox.ini               # Tox configuration
```

## Testing

- Write unit tests for all new functionality
- Maintain code coverage (aim for at least 80%)
- Run the full test suite before submitting a pull request

## Documentation

- Update relevant documentation for all changes
- Keep docstrings up-to-date
- Follow the existing documentation format

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).