import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="102203404-topsis",  # Package name should be unique and descriptive
    version="1.0.5",           # Initial version of your package
    description="A Python package to implement the TOPSIS decision-making method.",  # Short description
    long_description=README,   # Long description from README.md
    long_description_content_type="text/markdown",  # Content type for README
    url="https://github.com/Aryanz01/topsis-python-package",  # Replace with your actual GitHub repo URL
    author="Aryan Sabharwal",  # Your name
    author_email="asabharwal_be22@thapar.edu",  # Your email
    license="MIT",             # License type
    packages = find_packages(),
    install_requires=[],
)