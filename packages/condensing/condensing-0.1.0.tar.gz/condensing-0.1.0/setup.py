
from setuptools import setup, find_packages

setup(
    name="condensing",            # Package name
    version="0.1.0",             # Version number
    packages=find_packages(),    # Automatically find sub-packages
    description="A package to compute the mean of a dataset.",
    author="Your Name",
    author_email="your.email@example.com",
    install_requires=['numpy'],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points = {
        "console_scripts": [
            "condensing = condensing:is_homogeneous"
        ],
    },
)