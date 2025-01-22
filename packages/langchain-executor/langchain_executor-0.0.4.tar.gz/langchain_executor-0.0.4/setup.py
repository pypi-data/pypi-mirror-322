from pathlib import Path

from setuptools import find_packages, setup


def parse_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]


# Read dependencies from requirements.txt
install_requires = parse_requirements("requirements.txt")

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="langchain-executor",
    version="0.0.4",
    author="Yash Jain",
    author_email="yash0307jain@gmail.com",
    description="Langchain Executor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/yash0307jain/langchain-executor",
    install_requires=install_requires,
)
