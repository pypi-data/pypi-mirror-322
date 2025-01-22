from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="102203658_Suvit_Kumar",  # Replace with your package name
    version="1.0.2",  # Your current version
    author="Suvit Kumar",
    author_email="skumar5_be22@thapar.edu",
    description="A Python implementation of the TOPSIS method for multi-criteria decision making.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/102203658-Suvit-Kumar/1.0.1/",  # Replace with your PyPI package URL
    packages=find_packages(),
    install_requires=[
        # List any dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
