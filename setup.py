from setuptools import find_packages, setup

setup(
    name="flows",
    version="0.0.0",
    description="Prefect examples running self-contained in a local kubernetes cluster",
    python_requires=">=3.10",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["py.typed"],
    },
    install_requires=[
        # bokeh is needed for the dask dashboard
        "bokeh==2.4.3",
        "dask_kubernetes==2022.10.0",
        "prefect==2.10.20",
        "prefect-dask==0.2.1",
        "prefect-ray==0.2.0.post2",
        "prefect-shell==0.1.2",
        # required to read and write flows stored in minio
        "s3fs~=2022.3",
    ],
    extras_require={
        "dev": [
            "autoflake~=1.4",
            "black~=22.6",
            "build~=0.7",
            "isort~=5.9",
            "flake8~=5.0",
            "flake8-annotations~=2.7",
            "flake8-colors~=0.1",
            "pre-commit~=2.15",
            "pytest~=7.1",
        ]
    },
)
