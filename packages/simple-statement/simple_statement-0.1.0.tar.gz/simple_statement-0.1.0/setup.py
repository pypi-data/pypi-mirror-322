from setuptools import setup, find_packages

setup(
    name="simple_statement",  # Package name
    version="0.1.0",       # Initial version
    author="ejm",
    author_email="erikjmason@gmail.com",
    description="A simple package that prints a custom message",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/hello_printer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Minimum Python version
)
