"""Setup script for the Grub Kernel Updater package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grub-kernel-updater",
    version="0.2.0",
    author="Thomas Vincent",
    author_email="thomasvincent@gmx.com",
    description="A utility for managing GRUB boot configuration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomasvincent/grub-kernel-updater",
    project_urls={
        "Bug Tracker": "https://github.com/thomasvincent/grub-kernel-updater/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Boot",
        "Topic :: System :: Systems Administration",
        "Intended Audience :: System Administrators",
        "Development Status :: 4 - Beta",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "grub-kernel-updater=grub_kernel_updater.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "tox>=4.0.0",
        ],
    },
)