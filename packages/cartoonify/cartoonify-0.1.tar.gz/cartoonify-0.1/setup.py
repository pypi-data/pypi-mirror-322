from setuptools import setup, find_packages

setup(
    name='cartoonify',  # Replace with the name of your package
    version='0.1',  # The initial version of your package
    packages=find_packages(),  # Automatically finds all packages (including subdirectories like 'cartoonify')
    install_requires=[  # Add any dependencies here if necessary
        'opencv-python',  # Example of a required package
    ],
    classifiers=[  # Optional: Used for categorization in the Python Package Index (PyPI)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Use your license here
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Ensure compatibility with Python 3.6+
)
