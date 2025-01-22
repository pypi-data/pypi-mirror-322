from setuptools import setup, find_packages

setup(
    name="unique-linear-solver",  # Replace with your package name
    version="1.0.1",  # First release version
    description="A Python library for solving linear equations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rajeev Ranjan Pandey",
    author_email="rajeevr.kgp@gmail.com",
    url="https://github.com/rajeevranjanpandey/unique-linear-solver",
    packages=find_packages(),
    install_requires=["numpy"],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
