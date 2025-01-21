from setuptools import setup, find_packages

setup(
    name='vishesh',  # Make sure this name is unique on PyPI
    version='0.1',  # Update the version number
    description='A package to fetch and download programs from GitHub repository',
    author='Vishesh Jain',
    author_email='visheshj2005@gmail.com',
    url='https://github.com/visheshj2005/leetcode',  # Your GitHub repository URL
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vishesh = vishesh_helloworld.main:main',  # Make sure 'main' function is correctly referenced
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
