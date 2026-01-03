from setuptools import find_packages, setup
from typing import List

# Function to read requirements from requirements.txt
def get_requirements(file_path: str) -> List[str]:
    """
    Returns a list of requirements.
    Removes '-e .' if present.
    """
    requirements = []
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.strip() for req in requirements]

        if "-e ." in requirements:
            requirements.remove("-e .")

    return requirements


setup(
    name="music system",
    version="0.1.0",
    author="Prajwal Jagtap",
    author_email="prajwaljagtap977@gmail.com",
    description="A Machine Learning Web Application",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
