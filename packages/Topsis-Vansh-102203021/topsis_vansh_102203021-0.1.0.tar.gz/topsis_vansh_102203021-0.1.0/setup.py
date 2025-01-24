from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:  # Explicit UTF-8 encoding
    long_description = fh.read()

setup(
    name="Topsis-Vansh-102203021",
    version="0.1.0",
    author="Vansh",
    author_email="vansh@example.com",
    description="A Python package to implement the Topsis method.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
