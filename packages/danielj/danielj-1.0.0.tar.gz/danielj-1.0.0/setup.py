from setuptools import setup, find_packages

setup(
    name="danielj",
    version="1.0.0",
    author="Your Name",
    description="A library for weather forecasting and plotting tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/danielj",  # Replace with your GitHub URL
    packages=find_packages(),
    install_requires=[
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
