from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'pfdcm_tagextract',
    version          = '0.1',
    description      = 'An app to ...',
    long_description = readme,
    author           = 'Mohit Chandarana',
    author_email     = 'chandarana.m@northeastern.edu',
    url              = 'http://wiki',
    packages         = ['pfdcm_tagextract'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'pfdcm_tagextract = pfdcm_tagextract.__main__:main'
            ]
        }
)
