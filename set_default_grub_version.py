import os
import re
import subprocess


class GrubConf:
    """
    A class that encapsulates functionality related to the grub configuration file.
    """

    def __init__(self, path):
        """
        Initializes a new instance of the GrubConf class.

        Args:
            path (str): The path to the grub configuration file.
        """
        self.path = path

    def get_kernel_versions(self):
        """
        Extracts the versions of kernels from the grub configuration file.

        Returns:
            A list of version strings.
        """
        versions = []

        with open(self.path) as grub_file:
            for line in grub_file:
                match = re.search(r'kernel /boot/vmlinuz-([\d.]*)', line)
                if match:
                    version = match.group(1).strip()
                    if version:
                        versions.append(version)

        return versions

    def set_default_kernel_version(self, version):
        """
        Sets the default kernel version in the grub configuration file.

        Args:
            version (str): The kernel version to set as the default.
        """
        # Use fileinput to safely modify the file
        with fileinput.FileInput(self.path, inplace=True) as file:
            for line in file:
                # Replace the default kernel with the specified version
                line = re.sub(r"^default=.*", f"default={version}", line)
                print(line, end="")

        # Use check_call to execute the command safely
        subprocess.check_call(["/usr/bin/sed", "-i.bak", f"s/default=./default={version}/g", self.path])


class App:
    """
    A class that encapsulates the application logic for setting the default kernel version.
    """

    def __init__(self, conf):
        """
        Initializes a new instance of the App class.

        Args:
            conf (GrubConf): An instance of the GrubConf class.
        """
        self.conf = conf

    def run(self):
        """
        The main entry point of the script.
        """
        versions = self.conf.get_kernel_versions()

        if not versions:
            print("No kernel versions found in GRUB configuration")
            return

        highest_version = sorted(versions, reverse=True)[0]

        self.conf.set_default_kernel_version(highest_version)


if __name__ == "__main__":
    GRUB_PATH = "/etc/grub.conf"
    if not os.path.exists(GRUB_PATH):
        raise FileNotFoundError(f"{GRUB_PATH} does not exist")

    conf = GrubConf(GRUB_PATH)
    app = App(conf)
    app.run()
