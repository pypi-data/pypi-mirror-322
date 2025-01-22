from setuptools import setup, find_packages

setup(
    name="bloom-client",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python client for the Bloom Engine API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bloom-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests"
    ],
)
