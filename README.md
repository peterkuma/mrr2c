# mrr2c

Convert Metek MRR-2 micro rain radar data files to NetCDF.

mrr2c is an open source program which converts Metek Micro Rain Radar 2 (MRR-2)
data to NetCDF. RAW, PRO and AVE files are supported.

**Note:** Previous versions produced HDF5 files. If you need this type of output
for compatibility, use mrr2c version 1.0.3.

## Usage

mrr2c is a command line program to be run a terminal (Linux and macOS) or the
Command Prompt (Windows).

Synopsis:

`mrr2c` [`--debug`] [`-s`] *input* *output* \
`mrr2c` `-h`|`--help` \
`mrr2c` `-v`|`--version`

Converts data in the MRR-2 file *input* to a NetCDF file *output*.

Arguments:

- *input*: Input MRR-2 `.raw`, `.pro` or `.ave` file.
- *output*: Output NetCDF (`.nc`) file.

Options:

- `--debug`: Enable debugging output.
- `-h`, `--help`: Show help message and exit.
- `-s`: Split output into multiple files by vertical levels used. If the input
  file contains time periods with differing vertical levels, these time periods
  are saved separately in multiple files. If this option is set, *output* is
  assumed to be an output file prefix in the following way. If multiple sets of
  vertical levels are present, the output file names are *output*`_`*n*`.nc`,
  where *n* is a sequence of zero-prefixed numbers starting with 1, with a
  constant number of digits as needed to accommodate the entire sequence of
  files. If only one set of vertical levels is present, the output file name is
  *output*`.nc`.
- `-v`, `--version`: Print the version number and exit.

On Linux and macOS, see also the manual page:

```sh
man mrr2c
```

### Examples

Convert MRR-2 processed data in `0220.pro` to a NetCDF file `0220.pro`.

```sh
mrr2c 0220.pro 0220.nc
```

It is possible to use [GNU Parallel](https://www.gnu.org/software/parallel/) to
convert multiple files in parallel if you have more than one CPU core. For
example, to convert all `.pro` files in the current directory:

```sh
parallel mrr2c {} {.}.nc ::: *.pro
```

## Installation

It is recommended to run mrr2c on Linux.

### Linux

On Debian-derived distributions (Ubuntu, Devuan, ...), install the required
system packages with:

```sh
sudo apt install python3 python3-pip pipx
```

On Fedora, install the required system packages with:

```sh
sudo yum install python3 pipx
```

Install mrr2c:

```sh
pipx install mrr2c
mkdir -p ~/.local/share/man/man1
ln -s ~/.local/pipx/venvs/mrr2c/share/man/man1/mrr2c.1 ~/.local/share/man/man1/
```

Make sure that `$HOME/.local/bin` is included in the `PATH` environment
variable if not already. This can be done with `pipx ensurepath`.

You should now be able to run `mrr2c` and see the manual page with `man mrr2c`.

To uninstall:

```sh
pipx uninstall mrr2c
rm ~/.local/share/man/man1/mrr2c.1
```

### macOS

Open the Terminal. Install mrr2c with:

```sh
python3 -m pip install mrr2c
```

Make sure that `/Users/<user>/Library/Python/<version>/bin` is included in the
`PATH` environment variable if not already, where `<user>` is your system
user name and `<version>` is the Python version. This path should be printed
by the above command. This can be done by adding this line to the file
`.zprofile` in your home directory and restart the Terminal:

```sh
PATH="$PATH:/Users/<user>/Library/Python/<version>/bin"
```

You should now be able to run `mrr2c` and see the manual page with `man mrr2c`.

To uninstall:

```sh
python3 -m pip uninstall mrr2c
```

### Windows

Install [Python 3](https://www.python.org). In the installer, tick `Add
python.exe to PATH`.

Open Command Prompt from the Start menu. Install mrr2c with:

```sh
pip install mrr2c
```

You should now be able to run `mrr2c`.

To uninstall:

```sh
pip uninstall mrr2c
```

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

### 2.2.4 (2023-11-09)

- Fixed processing of profiles with zero or one profile with the `-s` option.
- Small improvements in the documentation.

### 2.2.3 (2023-11-08)

- Added option for splitting output into multiple files by vertical levels used.
- Improved documentation and manual page.

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
[ccbrowse](https://github.com/peterkuma/ccbrowse),
[cl2nc](https://github.com/peterkuma/cl2nc),
[mpl2nc](https://github.com/peterkuma/mpl2nc)
