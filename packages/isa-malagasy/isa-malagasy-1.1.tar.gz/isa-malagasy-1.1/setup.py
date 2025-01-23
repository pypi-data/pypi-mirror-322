from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="isa-malagasy",
    version="1.1",
    packages=find_packages(),
    description="Une bibliothèque pour convertir les nombres en lettres en malagasy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Day Lamiy",
    author_email="hatsudai1@gmail.com",
    url="https://github.com/Daylamiy06",
    license="Propriétaire",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
