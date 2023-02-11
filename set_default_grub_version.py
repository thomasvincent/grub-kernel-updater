import re
import os

GRUB_PATH = "/etc/grub.conf"

def get_available_versions():
    """
    Extracts the versions of kernels from the grub configuration file.

    Returns:
        A list of version strings.
    """
    versions = []

    with open(GRUB_PATH) as grub_file:
        for line in grub_file:
            match = re.search('kernel /boot/vmlinuz-([\d.]*)', line)
            if match:
                version = match.group(1).strip()
                if version:
                    versions.append(version)

    return versions


def get_highest_index(versions):
    """
    Finds the index of the highest version in the list of versions.

    Args:
        versions (list): A list of version strings.

    Returns:
        The index of the highest version in the list.
    """
    highest_version = 0

    for i, version in enumerate(versions,1):
        if version > versions[highest_version]:
            highest_version = i

    return highest_version


def main():
    """
    The main entry point of the script.
    """
    versions = get_available_versions()
    highest = get_highest_index(versions)

    command = f'sed -i.bak s/default=./default={highest}/g {GRUB_PATH}'
    os.system(command)

if __name__ == '__main__':
    main()
