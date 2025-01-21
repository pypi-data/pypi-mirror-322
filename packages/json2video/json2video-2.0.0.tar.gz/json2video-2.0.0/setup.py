from setuptools import setup, find_packages

setup(
    name="json2video",
    version="2.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
    author="JSON2Video.com",
    author_email="support@json2video.com",
    description="SDK for creating videos programmatically using JSON2Video API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://json2video.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 