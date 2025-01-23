import os
from setuptools import setup, find_packages

# Read the version from executor_plus/__version__.py
version = {}
with open(os.path.join("executor_plus", "__version__.py")) as fp:
    exec(fp.read(), version)

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="executor_plus",
    version=version["__version__"],  # Dynamically loaded version
    author="Yuting Zhang",
    author_email="opensource@yuting.link",
    description="An advanced executor library for Python with progress tracking, throttling, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/executor_plus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
)
