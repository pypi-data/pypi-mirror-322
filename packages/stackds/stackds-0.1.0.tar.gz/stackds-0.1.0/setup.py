from setuptools import setup, find_packages

setup(
    name="stackds",
    version="0.1.0",
    author="Colourless-Chameleon",
    description="A simple stack data structure implementation in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Clourless-Chameleon",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
