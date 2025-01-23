from setuptools import setup, find_packages

setup(
    name='xlxml',  # Correct package name
    version='1.0.0',
    description='Convert Excel format to Xml format',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['openpyxl'],
)
