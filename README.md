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

- Python 3 or a compatible distribution of Python such as Anaconda

To install mrr2c and dependencies with the Python package manager:

```sh
pip3 install mrr2c
```

**Note:** Append `--user` to install in your home directory on an unix-like
operating system (make sure `~/.local/bin` is included in the `PATH`
environmental variable).

## Variables

Supported variables are listed in the table below.

Time is expressed as Julian date (fractional number of days since -4712-01-01
12:00 UTC, or -4713-11-24 12:00 UTC in the proleptic Gregorian calendar). To
calculate UNIX time (number of seconds since 1 January 1970 00:00), use the
formula `(time - 2440587.5)*86400`. The time zone depends on
the raw data. Use the `time_zone` variable to determine the offset.

Missing values are expressed as NaN in the floating point (float64) variables
and -9223372036854775808 in the integer (int64) variables. The `_FillValue`
and `missing_value` attributes of each numerical variable contain the
respective missing value.

| Variable | Units | Symbol | Description | Type |
| --- | --- | --- | --- | --- |
| attenuated_radar_reflectivity | dbZ | z | Attenuated radar reflectivity | float64 |
| averaging_time | s | AVE | Averaging time | float64 |
| band | 1 | | Band number | int64 |
| bandwidth | | BW | Bandwidth | float64 |
| calibration_constant | | CC | Calibration constant | float64 |
| device_serial_number | string | DSN | Device serial number | S16 |
| drop_size | mm | D | Drop size | float64 |
| fall_velocity | m.s<sup>-1</sup> | W | Fall velocity | float64 |
| firmware_version | string | DVS | Firmware version | S16 |
| height_resolution | m | STP | Height resolution | float64 |
| height | m | H | Height | float64 |
| level | 1 | | Level number | int64 |
| liquid_water_content | g.m<sup>-3</sup> | LWC | Liquid water content | float64 |
| path_integrated_attenuation | dB | PIA | Path integrated attenuation | float64 |
| processing_level | string | TYP | Processing level | S3 |
| radar_altitude | m | ASL | Radar altitude | float64 |
| radar_reflectivity | dbZ | Z | Radar reflectivity | float64 |
| rain_rate | mm.h<sup>-1</sup> | RR | Rain rate | float64 |
| sampling_rate | Hz | SMP | Sampling rate | float64 |
| service_version | string | SVS | Service version | S16 |
| spectral_drop_density | m<sup>-3</sup>.mm<sup>-1</sup> | N | Spectral drop density | float64 |
| spectral_reflectivity | dB | F | Spectral reflectivity | float64 |
| time_zone | string | | Time zone | S8 |
| time | days since -4713-11-24 UTC (`proleptic_gregorian` calendar) | | Time | float64 |
| total_spectra | 1 | MDQ3 | Number of total spectra | int64 |
| transfer_function | | TF | Transfer function | float64 |
| valid_spectra_percentage | % | MDQ1 | Percentage of valid spectra | float64 |
| valid_spectra | 1 | MDQ2 | Number of valid spectra | int64 |

### Attributes

| Attribute | Description |
| --- | --- |
| software | `mrr2c (https://github.com/peterkuma/mrr2c)` |
| version | Software version |
| created | Time when the file was created (ISO 8601 UTC) |

## Release Notes

### 2.1.1 (2021-12-11)

- Changed time variable calendar to proleptic\_gregorian.
- Dropped support for Python 2.

### 2.1.0 (2020-08-13)

- Improved units to be more consistent with UDUNITS.

### 2.0.2 (2020-08-12)

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
