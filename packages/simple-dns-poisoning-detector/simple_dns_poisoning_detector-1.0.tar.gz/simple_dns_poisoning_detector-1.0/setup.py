from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for the long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="simple-dns-poisoning-detector",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "scapy",
        "reportlab",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "dns_poisoning_detector=src.main:main",  # Update entry point here
        ],
    },
    # Metadata for PyPI
    author="Olúmáyòwá Akinkuehinmi",
    author_email="akintunero101@gmail.com",
    description="A tool to detect DNS poisoning attacks.",
    long_description=long_description,  # Use README content as long description
    long_description_content_type="text/markdown",  # Specify the format of README (Markdown in this case)
    url="https://github.com/akintunero/dns-poisoning-detector",  # Correct repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.6",
)
