# mrr2

Convert Metek MRR-2 data files to HDF5.

## Usage

    mrr2 <infile> <outfile>

Arguments:

- `infile` - MRR-2 raw, pro or ave file
- `outfile` - output file (HDF5)

## Install

It is recommended to use Linux or a unix-like operating system.

Requirements:

- Python 2
- numpy
- h5py
- pydash

Install:

    python setup.py install

or

    python setup.py install --user

for installation in the home directory.
