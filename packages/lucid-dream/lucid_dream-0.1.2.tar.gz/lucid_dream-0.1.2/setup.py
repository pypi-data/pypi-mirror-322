from setuptools import setup, find_packages

setup(
    name="lucid-dream",  # Name of the package
    version="0.1.2",  # Initial version
    packages=find_packages(),  # Automatically find packages
    install_requires=[],  # Add any dependencies here
    description="A package for simulating and enhancing lucid dreaming experiences.",
    long_description=open('README.md').read(),  # Read the long description from README
    long_description_content_type="text/markdown",  # Mark down for the README file
    author="Ishan Oshada",  # Author's name
    author_email="ishan.kodithuwakku.offcial@gmail.com",  # Author's email (replace with your own)
    url="https://github.com/ishanoshada/lucid-dream",  # Your GitHub repo URL (replace with your own)
    classifiers=[
        "Programming Language :: Python :: 3",  # Specify supported Python versions
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",  # OS compatibility
    ]
)
