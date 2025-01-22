from setuptools import setup, find_packages

setup(
    name="apikee",
    version="0.0.6",
    author="usmhic",
    description="ApiKee - A lightweight API key validation library for FastAPI",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    url="https://github.com/apikee-dev/apikee-python",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)