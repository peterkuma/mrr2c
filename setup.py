from setuptools import setup, find_packages

setup(
    name='mrr2c',
    version='1.0.3',
    packages=find_packages(),
    py_modules=['mrr2c'],
    entry_points={
        'console_scripts': ['mrr2c=mrr2c:main'],
    },
    description='Convert Metek MRR-2 data files to HDF',
    author='Peter Kuma',
    author_email='peter@peterkuma.net',
    data_files=[('share/man/man1', ['mrr2c.1'])],
    install_requires=[
        'pydash>=4.0.3',
        'numpy>=1.12.1',
        'h5py>=2.2.1',
    ],
    keywords=['metek', 'radar', 'mrr-2', 'hdf'],
    url='https://github.com/peterkuma/mrr2c',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ],
)
