from setuptools import setup, find_packages

setup(
    name="dejaq",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3",
    ],
    entry_points={
        "console_scripts": [
            "dejaq=dejaq.cli:main",
        ],
    },
)