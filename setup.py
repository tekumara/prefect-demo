from pathlib import Path

from setuptools import find_packages, setup

long_description = Path("README.md").read_text()

setup(
    name="flows",
    version="0.0.0",
    description="Prefect Orion examples",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["py.typed"],
    },
    install_requires=["prefect>=2.0a6"],
    extras_require={
        "dev": [
            "autoflake~=1.4",
            "black~=21.10b0",
            "build~=0.7",
            "isort~=5.9",
            "flake8~=4.0",
            "flake8-annotations~=2.7",
            "flake8-colors~=0.1",
            "pre-commit~=2.15",
            "pytest~=6.2",
        ]
    },
)
