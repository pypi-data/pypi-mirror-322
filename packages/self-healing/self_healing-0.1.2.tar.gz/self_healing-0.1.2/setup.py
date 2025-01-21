from setuptools import setup, find_packages

setup(
    name="self_healing",
    version="0.1.2",
    description="The Self-Healing Library is a Python tool that dynamically runs and patches code to recover from runtime errors using installed data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Arsam",
    author_email="ashouriarsamold@gmail.com",
    url="https://github.com/pythonAndCplusplus/self_healing",
    packages=find_packages(),
    install_requires=[
        "prompt_toolkit"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)