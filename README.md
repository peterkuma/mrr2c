# mrr2c

Convert Metek MRR-2 data files to HDF5.

## Usage

    mrr2c <infile> <outfile>

Arguments:

- `infile` - MRR-2 `raw`, `pro` or `ave` file
- `outfile` - output file (HDF5)

## Install

It is recommended to run mrr2c on Linux or a unix-like operating system.

Requirements:

- Python 2.7
- pip
- libhdf5
- Python packages:
    - numpy >= 1.12.1
    - h5py >= 2.2.1
    - pydash >= 4.0.3

Install required python packages with pip:

    pip install -r requirements.txt

Install mrr2c:

    python setup.py install

or

    python setup.py install --user

for installation in the home directory.

## Fields

The following fields are supported:

- `attenuated_radar_reflectivity` (dbZ)
- `averaging_time` (s)
- `bandwidth`
- `calibration_constant`
- `device_serial_number` (string)
- `drop_size` (mm)
- `fall_velocity` (m.s^-1)
- `firmware_version` (string)
- `height_resolution` (m)
- `height` (m)
- `level` (string)
- `liquid_water_content` (g.m^-3)
- `path_integrated_attenuation` (dB)
- `radar_altitude` (m)
- `radar_reflectivity` (dbZ)
- `rain_rate` (mm.h^-1)
- `sampling_rate` (Hz)
- `service_version` (string)
- `spectral_drop_density` (m^-3.mm^-1)
- `spectral_reflectivity` (dB)
- `time_zone` (string)
- `time` (string)
- `total_spectra`
- `transfer_function`
- `valid_spectra_percentage` (%)
- `valid_spectra`
