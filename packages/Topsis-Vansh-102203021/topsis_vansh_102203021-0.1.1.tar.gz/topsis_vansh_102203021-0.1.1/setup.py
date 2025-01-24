from setuptools import setup, find_packages

setup(
    name="Topsis-Vansh-102203021",
    version="0.1.1",
    author="Vansh",
    author_email="vanshkansal5@example.com",
    description="A Python package for implementing the TOPSIS decision-making method.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/k-vanshhh/topsis_python_package",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "openpyxl"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
