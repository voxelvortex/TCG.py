import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VoxelVortex",
    version="1.0",
    author="Michael Scalzetti, Matthew Sprague, Luca Pieples",
    author_email="maestromikecode@gmail.com",
    description="A python API wrapper for TCG Player",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/voxelvortex/TCG.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)