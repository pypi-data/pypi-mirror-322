
from setuptools import setup, find_packages

setup(
    name="sdvettave",
    version="0.1.0",
    description="ETL package for the connectivity team",
    long_description="",
    author="moustapha.cheikh",
    author_email="bounesadava@gmail.com",
    url="https://github.com/sadavaboune/mytower_etl",
    packages=find_packages(),
    install_requires=[
        "paramiko", 
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
    