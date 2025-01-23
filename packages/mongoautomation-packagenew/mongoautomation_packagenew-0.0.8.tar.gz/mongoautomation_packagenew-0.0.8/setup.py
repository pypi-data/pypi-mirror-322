from setuptools import setup, find_packages
from typing import List
import os
HYPEN_E_DOT='-e .'
def get_requirement(file_path: str) -> List[str]:
    """Read and parse a requirements file."""
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Skipping...")
        return []
    with open(file_path) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        if "-e ." in requirements:
            requirements.remove("-e .")
        return requirements

     
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()     
   

__version__ = "0.0.8"
REPO_NAME = "Mongo_DB_Connector_PYPI_Package"
PKG_NAME= "mongoautomation_packagenew"
AUTHOR_USER_NAME = "JisnaP"
AUTHOR_EMAIL = "jisna12@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=get_requirement("requirements.txt")
    )