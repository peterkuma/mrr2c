# mrr2c

Convert Metek MRR-2 data files to HDF.

## Usage

    mrr2c [--debug] <infile> <outfile>

Arguments:

- `infile` - MRR-2 `raw`, `pro` or `ave` file
- `outfile` - output file (HDF5)
- `debug` - enable debugging output

## Install

It is recommended to run mrr2c on Linux or a unix-like operating system.

Requirements:

- Python 2.7
- pip
- libhdf5

Python packages:

- numpy >= 1.12.1
- h5py >= 2.2.1
- pydash >= 4.0.3

To install with the Python package manager
(automatically installs required packages):

    pip install mrr2c

To install from source:

    pip install numpy h5py pydash
    python setup.py install

## Variables

Supported variables are listed in the table below.

| Variable | Units | Symbol | Description |
| --- | --- |
| attenuated_radar_reflectivity | dbZ | z | Attenuated radar reflectivity |
| averaging_time | s | AVE | Averaging time |
| bandwidth | | BW | Bandwidth |
| calibration_constant | | CC | Calibration constant |
| device_serial_number | string | DSN | Device serial number |
| drop_size | mm | D | Drop size |
| fall_velocity | m.s<sup>-1</sup> | W | Fall velocity |
| firmware_version | string | DVS | Firmware version |
| height_resolution | m | STP | Height resolution |
| height | m | H | Height |
| level | string | TYP | Processing level |
| liquid_water_content | g.m<sup>-3</sup> | LWC | Liquid water content |
| path_integrated_attenuation | dB | PIA | Path integrated attenuation |
| radar_altitude | m | ASL | Radar altitude |
| radar_reflectivity | dbZ | Z | Radar reflectivity |
| rain_rate | mm.h<sup>-1</sup> | RR | Rain rate |
| sampling_rate | Hz | SMP | Sampling rate |
| service_version | string | SVS | Service version |
| spectral_drop_density | m<sup>-3</sup>.mm<sup>-1</sup> | N | Spectral drop density |
| spectral_reflectivity | dB | F | Spectral reflectivity |
| time_zone | string | Time zone |
| time | ISO 8601 | Time |
| total_spectra | | MDQ3 | Number of total spectra |
| transfer_function | | TF | Transfer function |
| valid_spectra_percentage | % | MDQ1 | Percentage of valid spectra |
| valid_spectra | | MDQ2 | Number of valid spectra |

## Release Notes

### 1.0.1 (2017-09-30)

- PyPI package.
- Improved documentation.

### 1.0 (2017-06-09)

- Initial release.

## License

MIT license (see [LICENSE.md](LICENSE.md))

## Contact

Peter Kuma <<peter.kuma@fastmail.com>>

## See also

[ALCF](https://alcf-lidar.github.io),
[ccplot](https://ccplot.org),
[cl2nc](https://github.com/peterkuma/cl2nc),
[mpl2nc](https://github.com/peterkuma/mpl2nc)
