from setuptools import setup, find_packages
from os import path

working_dir = path.abspath(path.dirname(__file__))

with open(path.join(working_dir,'readme.md'), encoding='utf-8') as f:
    long_description = f.read()
    
    
setup(
    name='check_execution_time_of_program',
    version='1.1.4',
    author='white_hat25',
    author_email='devmarcel30@gmail.com',
    description='A simple package to calculate the execution time of a program',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir = {"": "src"},
    packages=find_packages(where="src"),
    install_requires=[] 
)