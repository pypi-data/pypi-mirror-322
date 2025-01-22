from pathlib import Path

from setuptools import find_packages, setup


# Function to read the contents of the requirements.txt file
def parse_requirements(file_name):
    with open(file_name, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="langchain-executor",
    version="0.0.2",
    author="Yash Jain",
    author_email="yash0307jain@gmail.com",
    description="Langchain Executor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/yash0307jain/langchain-executor",
    install_requires=parse_requirements("requirements.txt"),
)
