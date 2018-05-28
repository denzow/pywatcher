# coding: utf-8

from setuptools import setup, find_packages

__VERSION__ = '0.5.0'


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_txt = f.read()

setup(
    name='pywatcher',
    version=__VERSION__,
    description='monitor file and reload process. like gulp watch.',
    long_description=readme,
    entry_points={
        "console_scripts": [
            "pywatcher = pywatcher.command:main"
        ]
    },
    author='denzow',
    author_email='denzow@gmail.com',
    url='https://github.com/denzow/pywatcher',
    license=license_txt,
    packages=find_packages(exclude=('example',)),
    install_requires=['watchdog'],
)
