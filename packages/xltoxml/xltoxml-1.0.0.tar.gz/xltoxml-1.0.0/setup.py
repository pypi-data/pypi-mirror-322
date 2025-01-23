from setuptools import setup, find_packages

setup(
    name='xltoxml',  # Correct package name
    version='1.0.0',
    description='Convert Excel files to XML format',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['openpyxl'],
)

