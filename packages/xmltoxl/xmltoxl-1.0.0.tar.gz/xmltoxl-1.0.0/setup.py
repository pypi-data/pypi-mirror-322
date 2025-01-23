from setuptools import setup, find_packages

setup(
    name='xmltoxl',  # Correct package name
    version='1.0.0',
    description='Convert Xml format to Excel format',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['openpyxl'],
)

