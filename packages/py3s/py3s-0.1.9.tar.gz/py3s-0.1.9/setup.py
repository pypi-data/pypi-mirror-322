from setuptools import setup

with open('version.txt', 'r') as f:
    version = f.read().strip("v\n\r\t ")

setup(
    name='py3s',
    version=version,
    packages=['py3s'],
    install_requires=[
        # List your package dependencies here
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dwdwow/py3s',
)
