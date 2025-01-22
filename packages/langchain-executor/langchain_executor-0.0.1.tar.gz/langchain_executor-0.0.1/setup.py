from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="langchain-executor",
    version="0.0.1",
    author="Yash Jain",
    author_email="yash0307jain@gmail.com",
    description="Langchain Executor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/yash0307jain/langchain-executor",
)
