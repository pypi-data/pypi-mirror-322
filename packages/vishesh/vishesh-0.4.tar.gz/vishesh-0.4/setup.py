# setup.py
from setuptools import setup, find_packages

setup(
    name="vishesh",
    version="0.4",
    description="LeetCode Problem Helper Tool",
    author="Vishesh Jain",
    author_email="visheshj2005@gmail.com",
    url="https://github.com/visheshj2005/leetcode",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "vishesh = vishesh.main:main",
        ],
    },
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
