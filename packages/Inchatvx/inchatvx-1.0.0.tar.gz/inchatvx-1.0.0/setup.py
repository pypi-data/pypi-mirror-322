from setuptools import setup, find_packages

setup(
    name="Inchatvx",
    version="1.0.0",
    author="Vermouth",
    author_email="Vermouth@gmail.com",
    description="A Python library for interacting with the InChat API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vermouth4/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
)
