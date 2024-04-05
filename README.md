# Grub Default Kernel Updater (Improved)

This Python script simplifies the process of updating the default kernel boot option in your GRUB configuration file.

## Requirements

- Python 3.9 or later (check with `python3 --version`)

**Important Note:**

Running this script requires root privileges, as it modifies system configuration files. Exercise caution and consider creating a system backup before proceeding.

## Usage

1. **Install Required Packages:**

   Ensure you have the necessary Python modules (`re` and `subprocess`) installed. If not, use your system's package manager (e.g., `apt-get install python3-re python3-subprocess` for Debian/Ubuntu).

2. **Download the Script:**

   Download the script (e.g., `grub_config_updater.py`) and save it to a suitable location.

3. **Run the Script (with Caution):**

   Open a terminal, navigate to the directory where you saved the script, and execute it with elevated privileges using `sudo`:

   ```bash
   sudo python3 grub_config_updater.py
   ```
   
Warning: Running the script with sudo grants it root access. Double-check that you're using the correct script before proceeding.

## Features

- Enhanced Error Handling: The script now gracefully handles potential errors, such as missing configuration files or invalid kernel version formats.
- Configurable Default Kernel Selection: (Optional) You can modify the script's logic to select a specific kernel version as the default, providing more customization (see "Future Improvements").
- Support for Different GRUB File Paths: (Optional) The script can be extended to accommodate various GRUB configuration file locations (see "Future Improvements").

## Limitations

Specific GRUB Format Assumption: The script currently assumes a particular format for GRUB configuration files (lines starting with kernel /boot/vmlinuz-). This might need adjustments depending on your system's setup.
Future Improvements

## User Input for Default Kernel Version:
Allow users to specify the desired default kernel version via command-line arguments.
Support for Varying GRUB Paths: Enable configuration of the GRUB configuration file path based on user or system settings.
GRUB Version Detection: Potentially detect the GRUB version and adapt accordingly (advanced).
