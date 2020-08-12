# mrr2c

Convert Metek MRR-2 micro rain radar data files to NetCDF.

mrr2c is an open source program which converts Metek Micro Rain Radar 2 (MRR-2)
data to NetCDF. RAW, PRO and AVE files are supported.

**Note:** Previous versions produced HDF5 files. If you need this type of output
for compatibility, use mrr2c version 1.0.3.

## Usage

```sh
mrr2c [--debug] <input> <output>
```

Arguments:

- `input`: Input MRR-2 `.raw`, `.pro` or `.ave` file.
- `output`: Output NetCDF (`.nc`) file.

Options:

- `--debug`: Enable debugging output.

See also the man page:

```sh
man mrr2c
```

## Installation

It is recommended to run mrr2c on Linux or a unix-like operating system.

Requirements:

- Python 2.7 or 3 or a compatible distribution of Python such as Anaconda

To install mrr2c and dependencies with the Python package manager:

```sh
pip3 install mrr2c
```

**Note:** Replace `pip3` with `pip` to install with Python 2.7.

**Note:** Append `--user` to install in your home directory on an unix-like
operating system (make sure `~/.local/bin` is included in the `PATH`
environmental variable).

## Variables

Supported variables are listed in the table below.

Time is expressed as Julian date. To calculate UNIX time (number of seconds
since 1970-01-01 00:00), use the formula `(time - 2440587.5)*86400`.

| Variable | Units | Symbol | Description |
| --- | --- | --- | --- |
| attenuated_radar_reflectivity | dbZ | z | Attenuated radar reflectivity |
| averaging_time | s | AVE | Averaging time |
| band | 1 | Band number |
| bandwidth | | BW | Bandwidth |
| calibration_constant | | CC | Calibration constant |
| device_serial_number | string | DSN | Device serial number |
| drop_size | mm | D | Drop size |
| fall_velocity | m.s<sup>-1</sup> | W | Fall velocity |
| firmware_version | string | DVS | Firmware version |
| height_resolution | m | STP | Height resolution |
| height | m | H | Height |
| level | 1 | | Level number |
| liquid_water_content | g.m<sup>-3</sup> | LWC | Liquid water content |
| path_integrated_attenuation | dB | PIA | Path integrated attenuation |
| processing_level | string | TYP | Processing level |
| radar_altitude | m | ASL | Radar altitude |
| radar_reflectivity | dbZ | Z | Radar reflectivity |
| rain_rate | mm.h<sup>-1</sup> | RR | Rain rate |
| sampling_rate | Hz | SMP | Sampling rate |
| service_version | string | SVS | Service version |
| spectral_drop_density | m<sup>-3</sup>.mm<sup>-1</sup> | N | Spectral drop density |
| spectral_reflectivity | dB | F | Spectral reflectivity |
| time_zone | string | | Time zone |
| time | days since -4712-01-01T12:00:00 | | Time |
| total_spectra | | MDQ3 | Number of total spectra |
| transfer_function | | TF | Transfer function |
| valid_spectra_percentage | % | MDQ1 | Percentage of valid spectra |
| valid_spectra | | MDQ2 | Number of valid spectra |

### Attributes

| Attribute | Description |
| --- | --- |
| software | `mrr2c (https://github.com/peterkuma/mrr2c)` |
| version | Software version |
| created | Time when the file was created (ISO 8601 UTC) |

## Release Notes

### 2.0.0 (2020-08-11)

- Support for Python 3.
- Changed output format to NetCDF.
- Changed variable time to numerical.
- Added variable level.
- Named dimensions.
- Added ancillary attributes.

### 1.0.3 (2020-07-18)

- Fixed installation on Windows.

### 1.0.2 (2020-02-02)

- Add man page.

### 1.0.1 (2017-09-30)

- PyPI package.
- Improved documentation.

### 1.0 (2017-06-09)

- Initial release.

## License

mrr2c can be used, modified and distributed freely under the terms
of an MIT license (see [LICENSE.md](LICENSE.md)).

## Contact

Please contact Peter Kuma <<peter@peterkuma.net>> regarding support
or bugs or use the GitHub Issues.

## See also

[ALCF](https://alcf-lidar.github.io),
[ccplot](https://ccplot.org),
[cl2nc](https://github.com/peterkuma/cl2nc),
[mpl2nc](https://github.com/peterkuma/mpl2nc)
