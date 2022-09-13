from setuptools import find_packages, setup

setup(
    name="flows",
    version="0.0.0",
    description="Prefect Orion examples running self-contained in a local kubernetes cluster",
    python_requires=">=3.9",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["py.typed"],
    },
    install_requires=[
        # bokeh is needed for the dask dashboard
        "bokeh",
        "boto3==1.21.21",
        "dask_kubernetes",
        "prefect==2.3.2",
        "prefect-dask",
        "prefect-ray",
        "prefect-shell",
    ],
    extras_require={
        "dev": [
            "autoflake~=1.4",
            "black~=22.6",
            "build~=0.7",
            "isort~=5.9",
            "flake8~=4.0",
            "flake8-annotations~=2.7",
            "flake8-colors~=0.1",
            "pre-commit~=2.15",
            "pytest~=6.2",
            "s3fs~=2022.3",
        ]
    },
)
