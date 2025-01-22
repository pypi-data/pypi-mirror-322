from setuptools import setup, find_packages

# Set up the package
setup(
    name="shivduttchoubey",
    version="0.1.0",
    packages=find_packages(),
    description="A package to open Shivdutt Choubey's website",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shivdutt Choubey",
    author_email="your.email@example.com",  # Replace with your email
    url="https://github.com/shivduttchoubey/shivduttchoubey",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)