import setuptools
import os

FILEPATH = os.path.abspath(os.path.dirname(__file__)) + '/'

setuptools.setup(
    name='chiliserver',
    version='1.0.0',
    author='Joni Koskinen',
    author_email='joni.m.koskinen@gmail.com',
    packages=setuptools.find_packages(),
    long_description=open('README.txt', 'r').read(),
    install_requires=['psycopg2']
)