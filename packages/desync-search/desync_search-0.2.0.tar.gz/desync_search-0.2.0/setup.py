from setuptools import setup, find_packages

setup(
    name="desync_search",
    version="0.2.0",  # bumped from 0.1.x due to major changes
    author="Maksymilian Kubicki",
    author_email="maks@desync.ai",
    description="API for the internet",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/notyetcreated/desync_search",  # or your link
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "requests>=2.25.0"
    ],
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
