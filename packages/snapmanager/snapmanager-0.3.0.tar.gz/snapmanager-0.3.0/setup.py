"""Setup script for snapmanager."""
from setuptools import setup, find_packages

setup(
    name="snapmanager",
    version="0.3.0",
    description="Makes VSS snapshot disks bootable in Google Cloud",
    author="Ali Aktas",
    packages=find_packages(),
    install_requires=[
        "google-cloud-compute>=1.23.0",
        "rich>=10.0.0",
        "pywinrm>=0.4.3",
        "click>=8.0.0"
    ],
    entry_points={
        'console_scripts': [
            'snapmanager=snapmanager.cli:main',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Systems Administration",
    ],
)
