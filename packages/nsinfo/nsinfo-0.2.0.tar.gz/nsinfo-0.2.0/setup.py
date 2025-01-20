from setuptools import setup, find_packages

setup(
    name="nsinfo",
    version="0.2.0",
    description="Une bibliothèque Python qui vise à implémenter ce qu'on utilise en NSI (Piles, Files, Graphes, etc.)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="TataneSan",
    author_email="admin@tatanesan.fr",
    url="https://github.com/TataneSan/nsi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)