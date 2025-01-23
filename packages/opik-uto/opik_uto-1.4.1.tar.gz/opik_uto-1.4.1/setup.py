from setuptools import setup, find_packages

setup(
    name="opik_uto",
    version="1.4.1",
    author="Henrry",
    packages=find_packages(),
    python_requires=">=3.9,<3.13",
    platforms=["Windows", "Linux", "MacOS"],
    install_requires=[
        "levenshtein==0.25.1",
        "python-dateutil==2.9.0.post0",
        "pandas==2.2.3",
        "rapidfuzz==3.11.0",
        "uuid7==0.1.0",
    ],
)