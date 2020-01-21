import os.path
from setuptools import setup, find_packages

VERSION = "0.1.0"
HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="aws-emr-launcher",
    version=VERSION,
    description="Library that enables to provision EMR clusters with yaml config files (Configuration as Code)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/HarshadRanganathan/aws-emr-launcher",
    author="Harshad Ranganathan",
    author_email="rharshad93@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="AWS EMR",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "boto3"
    ],
    python_requires='>=3.7',
)
