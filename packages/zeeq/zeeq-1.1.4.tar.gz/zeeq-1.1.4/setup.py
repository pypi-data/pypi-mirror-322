from setuptools import setup, find_packages

setup(
    name="zeeq",
    version="1.1.4",  # Update version for new releases
    author="Athish NS",
    author_email="athishnsofficial@gmail.com",
    description="A natural language interface for quantum programming using Cirq.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/athish-ns/zeeq",  # Link to your GitHub repository
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "cirq",
        "numpy",
        "logging",
        "matplotlib",

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.7",
)
