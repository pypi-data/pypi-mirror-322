from setuptools import setup, find_packages

setup(
    name="hiedwinlan",
    version="0.1.0",
    author="HiedwinLan",
    author_email="your.email@example.com",
    description="A simple SDK that returns Hello World",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hiedwinlan",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 