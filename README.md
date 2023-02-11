# Grub Config Updater

A Python script for updating the default boot option in the GRUB configuration file.

## Requirements
- Python 3.9 or higher
- The script must be run with root privileges, as it modifies the `/etc/grub.conf` file.

## Usage
``` python grub_config_updater.py ```

## Limitations
- The script assumes that the GRUB configuration file follows the specific format of listing the available kernels with the line starting with `kernel /boot/vmlinuz-`.
- The script assumes that the highest available version of the kernel is the one that should be set as the default.

## Future Improvements
- Add input validation and error handling
- Add command-line arguments to allow the user to specify which kernel version to set as the default.
- Add support for different GRUB configuration file paths.


