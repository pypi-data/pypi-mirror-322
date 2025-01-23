import setuptools
from setuptools import setup


with open("lectric/VERSION") as version_fh:
  version = version_fh.read().strip()

with open("README.md") as readme_fh:
  long_description = readme_fh.read()


setup(
    name='lectric-sdk',
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
    version=version,
    description='Lectric client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Disa Mhembere',
    author_email='disamhembere@microsoft.com',
    keywords=['lectric', 'vdb', 'vector database'],
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"],
    install_requires=[
        "setuptools>=41.0.1",
        "httpx>=0.23.0",
        "attrs>=21.4.0",
        "wheel",
        "requests",
        "numpy",
        "python-dateutil"
    ],
    zip_safe=False
)
