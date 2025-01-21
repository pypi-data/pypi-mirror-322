from setuptools import setup, find_packages

setup(
    name='vishesh',  # Package name you want to use on PyPI
    version='0.2',  # Version number
    description='A package to fetch and download programs from GitHub repository',
    author='Vishesh Jain',
    author_email='visheshj2005@gmail.com',  # Your email
    url='https://github.com/visheshj2005/leetcode',  # Your GitHub repository URL
    packages=find_packages(),  # This will automatically find the packages
    entry_points={
        'console_scripts': [
            'vishesh = vishesh.main:main',  # Adjusted to the correct function path
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',  # Specifies Python version compatibility
        'License :: OSI Approved :: MIT License',  # MIT License
        'Operating System :: OS Independent',  # OS compatibility
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
