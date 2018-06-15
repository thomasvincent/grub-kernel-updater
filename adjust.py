import re
import os

grub_path = "/etc/grub.conf"

def available_versions():
    versions = []

    with open(grub_path) as grub:
        for line in grub:
            m = re.search('kernel /boot/vmlinuz-([\d.]*)', line)
            if m:
                version = m.group(1).strip()
                if len(version) > 0:
                    versions.append(version)

    return versions


def highest_index(versions):
    highest_version = 0

    for i, version in enumerate(versions,1):
        if version > versions[highest_version]:
            highest_version = i

    return highest_version


def main():
    versions = available_versions()
    highest = highest_index(versions)

    command = 'sed -i.bak s/default=./default={}/g {}'.format(highest, grub_path)
    print(command)
    os.popen(command)


if __name__ == '__main__':
    main()
