from setuptools import setup, find_packages  # type: ignore
import os
import re


# Read version from __init__.py
def get_version():
    init_path = os.path.join(os.path.dirname(__file__), "airtrain", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="airtrain",
    version=get_version(),
    author="Dheeraj Pai",
    author_email="helloworldcmu@gmail.com",
    description="A platform for building and deploying AI agents with structured skills",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rosaboyle/airtrain.dev",
    packages=find_packages(include=["airtrain", "airtrain.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "PyYAML>=5.4.1",
        "firebase-admin>=5.0.0",  # Optional, only if using Firebase
        "loguru>=0.5.3",  # For logging
    ],
)
