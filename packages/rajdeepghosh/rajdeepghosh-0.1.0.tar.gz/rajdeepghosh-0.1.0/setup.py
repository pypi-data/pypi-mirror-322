from setuptools import setup, find_packages

setup(
    name="rajdeepghosh",
    version="0.1.0",
    packages=find_packages(),
    description="A package to open Rajdeep Ghosh's portfolio website",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rajdeep Ghosh",
    author_email="shivduttchoubey@gmail.com",  # Replace with your email
    url="https://github.com/rajghosh2000/rajdeepghosh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
