from setuptools import setup, find_packages

setup(
    name='mrr2c',
    version='1.0',
    packages=find_packages(),
    scripts=['mrr2c'],
    description='Convert Metek MRR-2 data files to HDF5',
    author='Peter Kuma',
    author_email='peter.kuma@fastmail.com',
)
