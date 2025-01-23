import pathlib
import setuptools

setuptools.setup(
    name='learn_addition',
    version='0.0.1',
    long_description=pathlib.Path('README.md').read_text(),
    packages=setuptools.find_packages(exclude=['Testing','Design']),
)