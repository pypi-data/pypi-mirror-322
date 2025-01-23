from pathlib import Path

from setuptools import setup, find_packages

VERSION = "2.2.2"  # PEP-440

NAME = "BulletPrompt"

INSTALL_REQUIRES = []


setup(
    name=NAME,
    version=VERSION,
    description="Beautiful Python prompts made simple. Maintained version of bchao1/bullet.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/danner26/BulletPrompt",
    project_urls={
        "Source Code": "https://github.com/danner26/BulletPrompt",
    },
    author="danner26",
    author_email="daniel.anner@danstechsupport.com",
    keywords="cli list prompt customize colors",
    license="MIT",
    python_requires=">=3.6",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)
