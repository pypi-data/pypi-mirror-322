from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="langchain-executor",
    version="0.0.3",
    author="Yash Jain",
    author_email="yash0307jain@gmail.com",
    description="Langchain Executor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/yash0307jain/langchain-executor",
    install_requires=[
        "langchain==0.3.14",
        "langchain-community==0.3.14",
        "langchain-core==0.3.30",
        "langchain-openai==0.3.0",
        "langchain-text-splitters==0.3.5",
    ],
)
