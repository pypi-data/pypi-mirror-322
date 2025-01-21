# setup.py
from setuptools import setup, find_packages

setup(
    name='vishesh-helloworld',  # Your package name
    version='0.1',  # Version of the package
    description='A package to create a simple hello world script',  # Short description of the package
    author='Vishesh Jain',  # Your name
    author_email='your_email@example.com',  # Your email (replace with actual)
    url='https://pypi.org/project/vishesh-helloworld/',  # URL to your PyPI package page
    packages=find_packages(),  # Automatically find packages in your project directory
    entry_points={  # Define the entry point for your console script
        'console_scripts': [
            'vishesh = vishesh_helloworld.main:create_helloworld_file',  # The command to run and function to call
        ],
    },
    classifiers=[  # Additional metadata about the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version requirement
)
