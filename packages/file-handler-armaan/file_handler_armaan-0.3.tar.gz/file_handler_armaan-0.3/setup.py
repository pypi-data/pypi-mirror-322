from setuptools import setup, find_packages

setup(
    name="file_handler_armaan",
    version="0.3",
    author="Armaan",
    author_email="your_email@example.com",
    description="A simple package for file handling in multiple formats",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file_handler",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],  # List of dependencies
    license="MIT",  # Correctly set license here
)
