# setup.py
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="AutodocStringFormater",
    version="0.1",
    description="A Python library to automatically generate docstrings for Python files.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify the content type
    author="Anivesh Nishad",
    author_email="anivesh.nishad76@gmail.com",
    packages=find_packages(),
    install_requires=["astor"],
    entry_points={
        "console_scripts": [
            "AutodocStringFormater=AutodocStringFormater:AutodocStringFormater",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)