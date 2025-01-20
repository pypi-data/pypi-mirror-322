from setuptools import setup, find_packages


setup(
    name="pyeqx-core",
    version="0.7.16",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "adlfs>=2024.2.0",
        "azure-identity>=1.13.0",
        "azure-storage-blob>=12.16.0",
        "azure-storage-file-datalake>=12.11.0",
        "azure-storage-queue>=12.6.0",
        "delta-spark>=3.2.0,<3.3.0",
        "minio>=7.2.3",
        "numpy>=1.26.0",
        "pandas>=2.2.0",
        "psycopg2-binary>=2.9.9",
        "pymssql>=2.2.11",
        "pyspark>=3.5.1",
        "requests>=2.30.0",
        "tenacity>=8.2.1",
    ],
    python_requires=">=3.11",
)
