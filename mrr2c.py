#!/usr/bin/env python

import sys
import argparse
import re
import logging
import pydash as py_
import numpy as np
import jdf
from jdf.na import *

FORMAT = {
    'MRR_RAW': re.compile(r'^MRR +(?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d) +(?P<time_zone>[^ ]+) +DVS +(?P<DVS>[^ ]+) +DSN +(?P<DSN>[^ ]+) +BW +(?P<BW>[^ ]+) +CC +(?P<CC>[^ ]+) +MDQ +(?P<MDQ1>[^ ]+) +(?P<MDQ2>[^ ]+) +(?P<MDQ3>[^ ]+) +TYP (?P<TYP>RAW)\s*$'),
    'MRR_AVE': re.compile(r'^MRR +(?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d) +(?P<time_zone>[^ ]+) +AVE +(?P<AVE>[^ ]+) +STP +(?P<STP>[^ ]+) +ASL +(?P<ASL>[^ ]+) +SMP +(?P<SMP>[^ ]+) +SVS +(?P<SVS>[^ ]+) +DVS +(?P<DVS>[^ ]+) +DSN +(?P<DSN>[^ ]+) +CC +(?P<CC>[^ ]+) +MDQ +(?P<MDQ1>[^ ]+) +TYP +(?P<TYP>AVE)\s*$'),
    'MRR_PRO': re.compile(r'^MRR +(?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d) +(?P<time_zone>[^ ]+) +AVE +(?P<AVE>[^ ]+) +STP +(?P<STP>[^ ]+) +ASL +(?P<ASL>[^ ]+) +SMP +(?P<SMP>[^ ]+) +SVS +(?P<SVS>[^ ]+) +DVS +(?P<DVS>[^ ]+) +DSN +(?P<DSN>[^ ]+) +CC +(?P<CC>[^ ]+) +MDQ +(?P<MDQ1>[^ ]+) +TYP +(?P<TYP>PRO)\s*$'),
}

FIELDS = {
    'RAW': [
        'bandwidth',
        'calibration_constant',
        'device_serial_number',
        'firmware_version',
        'height',
        'level',
        'spectral_reflectivity',
        'time',
        'time_zone',
        'total_spectra',
        'transfer_function',
        'valid_spectra',
        'valid_spectra_percentage',
    ],
    'AVE': [
        'attenuated_radar_reflectivity',
        'averaging_time',
        'calibration_constant',
        'device_serial_number',
        'drop_size',
        'fall_velocity',
        'firmware_version',
        'height',
        'height_resolution',
        'level',
        'liquid_water_content',
        'path_integrated_attenuation',
        'radar_altitude',
        'radar_reflectivity',
        'rain_rate',
        'sampling_rate',
        'service_version',
        'spectral_drop_density',
        'spectral_reflectivity',
        'time',
        'time_zone',
        'transfer_function',
        'valid_spectra_percentage',
    ],
    'PRO': [
        'attenuated_radar_reflectivity',
        'averaging_time',
        'calibration_constant',
        'device_serial_number',
        'drop_size',
        'fall_velocity',
        'firmware_version',
        'height',
        'height_resolution',
        'level',
        'liquid_water_content',
        'path_integrated_attenuation',
        'radar_altitude',
        'radar_reflectivity',
        'rain_rate',
        'sampling_rate',
        'service_version',
        'spectral_drop_density',
        'spectral_reflectivity',
        'time',
        'time_zone',
        'transfer_function',
        'valid_spectra_percentage',
    ]
}

MRR_TYPES = {
    'year': int,
    'month': int,
    'day': int,
    'hour': int,
    'minute': int,
    'second': int,
    'time_zone': str,
    'AVE': int,
    'STP': int,
    'ASL': int,
    'SMP': float,
    'SVS': str,
    'DVS': str,
    'DSN': str,
    'BW': int,
    'CC': int,
    'MDQ1': int,
    'MDQ2': int,
    'MDQ3': int,
    'TYP': str,
}

def format_time(year, month, day, hour, minute, second):
    return '20%(year)02d-%(month)02d-%(day)02dT%(hour)02d:%(minute)02d:%(second)02d' % locals()

def parse_mrr(s):
    for k, v in FORMAT.items():
        m = v.match(s)
        if m is not None:
            d = m.groupdict()
            return {
                k1: MRR_TYPES.get(k1, str)(v1)
                for k1, v1 in d.items()
            }
    return None

def parse_int(rec):
    return np.array([
        int(x) if x != '' else NA_INT64
        for x in rec[1:]]
    )

def parse_float(rec):
    return np.array([
        float(x) if x != '' else NA_FLOAT64
        for x in rec[1:]]
    )

def parse_spectral_float(rec):
    return [
        int(rec[0][1:]),
        np.array([
            float(x) if x != '' else NA_FLOAT64
            for x in rec[1:]]
        )
    ]

def parse_size(f):
    d = {
        'nprof': 0,
        'nlev': 0,
        'nspectral': 64,
    }

    def parse_line(line, d):
        if line.startswith('MRR'):
            d['nprof'] += 1
        if line.startswith('H'):
            d['nlev'] = max(d['nlev'], len(py_.split(py_.drop(line, 3))))

    for line_number, line in enumerate(f.readlines()):
        try:
            parse_line(line, d)
        except Exception as e:
            raise IOError, 'Error parsing line %d: %s' % (
                line_number + 1,
                unicode(e)
            ), sys.exc_info()[2]

    return d

def dataset_template(size):
    return {
        'time': {
            '$data': np.zeros(size['nprof'], dtype='S19'),
            '$attributes': {
                'long_name': 'time',
                'units': 'iso8601'
            }
        },
        'time_zone': {
            '$data': np.zeros(size['nprof'], dtype='S8'),
            '$attributes': {
                'long_name': 'time zone'
            }
        },
        'height': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev']), 'float64'),
            '$attributes': {
                'long_name': 'height',
                'units': 'm',
                'symbol': 'H'
            }
        },
        'transfer_function': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev']), 'float64'),
            '$attributes': {
                'long_name': 'transfer function',
                'symbol': 'TF'
            }
        },
        'spectral_reflectivity': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev'], size['nspectral']), 'float64'),
            '$attributes': {
                'long_name': 'spectral reflectivity',
                'units': 'dB',
                'symbol': 'F'
            }
        },
        'drop_size': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev'], size['nspectral']), 'float64'),
            '$attributes': {
                'long_name': 'drop size',
                'units': 'mm',
                'symbol': 'D'
            }
        },
        'spectral_drop_density': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev'], size['nspectral']), 'float64'),
            '$attributes': {
                'long_name': 'spectral drop density',
                'units': 'm^{-3} mm^{-1}',
                'symbol': 'N'
            }
        },
        'path_integrated_attenuation': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev']), 'float64'),
            '$attributes': {
                'long_name': 'path integrated attenuation',
                'units': 'dB',
                'symbol': 'PIA'
            }
        },
        'radar_reflectivity': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev']), 'float64'),
            '$attributes': {
                'long_name': 'radar reflectivity',
                'units': 'dBZ',
                'symbol': 'Z'
            }
        },
        'attenuated_radar_reflectivity': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev']), 'float64'),
            '$attributes': {
                'long_name': 'attenuated radar reflectivity',
                'units': 'dBZ',
                'symbol': 'z'
            }
        },
        'rain_rate': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev']), 'float64'),
            '$attributes': {
                'long_name': 'rain rate',
                'units': 'mm h^{-1}',
                'symbol': 'RR'
            }
        },
        'liquid_water_content': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev']), 'float64'),
            '$attributes': {
                'long_name': 'liquid water content',
                'units': 'g m^{-3}',
                'symbol': 'LWC'
            }
        },
        'fall_velocity': {
            '$data': NA_FLOAT64*np.ones((size['nprof'], size['nlev']), 'float64'),
            '$attributes': {
                'long_name': 'fall velocity',
                'units': 'm s^{-1}',
                'symbol': 'W'
            }
        },
        'calibration_constant': {
            '$data': NA_FLOAT64*np.ones(size['nprof'], 'float64'),
            '$attributes': {
                'long_name': 'calibration constant',
                'symbol': 'CC'
            }
        },
        'bandwidth': {
            '$data': NA_FLOAT64*np.ones(size['nprof'], 'float64'),
            '$attributes': {
                'long_name': 'bandwidth',
                'symbol': 'BW'
            }
        },
        'valid_spectra_percentage': {
            '$data': NA_FLOAT64*np.ones(size['nprof'], 'float64'),
            '$attributes': {
                'long_name': 'percentage of valid spectra',
                'units': 'percent',
                'symbol': 'MDQ1'
            }
        },
        'valid_spectra': {
            '$data': NA_INT64*np.ones(size['nprof'], 'int64'),
            '$attributes': {
                'long_name': 'number of valid spectra',
                'symbol': 'MDQ2'
            }
        },
        'total_spectra': {
            '$data': NA_INT64*np.ones(size['nprof'], 'int64'),
            '$attributes': {
                'long_name': 'number of total spectra',
                'symbol': 'MDQ3'
            }
        },
        'firmware_version': {
            '$data': np.zeros(size['nprof'], 'S16'),
            '$attributes': {
                'long_name': 'firmware version',
                'symbol': 'DVS'
            }
        },
        'service_version': {
            '$data': np.zeros(size['nprof'], 'S16'),
            '$attributes': {
                'long_name': 'service version',
                'symbol': 'SVS'
            }
        },
        'device_serial_number': {
            '$data': np.zeros(size['nprof'], 'S16'),
            '$attributes': {
                'long_name': 'device serial number',
                'symbol': 'DSN'
            }
        },
        'averaging_time': {
            '$data': NA_FLOAT64*np.ones(size['nprof'], 'float64'),
            '$attributes': {
                'long_name': 'averaging time',
                'units': 's',
                'symbol': 'AVE'
            }
        },
        'height_resolution': {
            '$data': NA_FLOAT64*np.ones(size['nprof'], 'float64'),
            '$attributes': {
                'long_name': 'height resolution',
                'units': 'm',
                'symbol': 'STP'
            }
        },
        'radar_altitude': {
            '$data': NA_FLOAT64*np.ones(size['nprof'], 'float64'),
            '$attributes': {
                'long_name': 'radar altitude above sea level',
                'units': 'm',
                'symbol': 'ASL'
            }
        },
        'sampling_rate': {
            '$data': NA_FLOAT64*np.ones(size['nprof'], 'float64'),
            '$attributes': {
                'long_name': 'sampling rate',
                'units': 'Hz',
                'symbol': 'SMP'
            }
        },
        'level': {
            '$data': np.zeros(size['nprof'], 'S3'),
            '$attributes': {
                'long_name': 'processing level',
                'symbol': 'TYP'
            }
        }
    }

def parse_line(line, d, size, fields, status):
    i = status['i']
    file_level = status['file_level']
    level = status['level']

    symbols = fields.keys()

    field_width = max(1, (len(line) - 3)/size['nlev'])
    rec = py_.concat(
        py_.trim(py_.take(line, 3)),
        py_.map_(py_.chunk(py_.drop(line, 3), field_width), lambda x: py_.trim(x))
    )

    if rec[0] == 'MRR':
        i = i + 1 if i is not None else 0
        res = parse_mrr(line)

        if res is None:
            raise IOError('Unrecognized line format')

        level = res['TYP']
        if file_level is not None and level != file_level:
            raise IOError('Mixed processing levels')
        else:
            file_level = res['TYP']

        d['time']['$data'][i] = format_time(**py_.pick(
            res,
            ('year', 'month', 'day', 'hour', 'minute', 'second')
        ))
        d['time_zone']['$data'][i] = res['time_zone']
        for k, v in res.items():
            if k in symbols:
                x = fields[k]
                name = x['name']
                d[name]['$data'][i] = v

    elif rec[0] in symbols or py_.nth(rec[0], 0) in symbols:
        if i is None or file_level is None:
            raise IOError('Unexpected line')

        if file_level is not None and level != file_level:
            raise IOError('Mixed processing levels')

        if rec[0] in symbols:
            x = fields[rec[0]]
        else:
            x = fields[py_.nth(rec[0], 0)]
        name = x['name']

        dtype = str(x['dtype'])
        if x['spectral'] is True:
            if dtype == 'float64':
                res = parse_spectral_float(rec)
            else:
                raise AssertionError('Invalid dtype %s' % dtype)
            if len(res[1]) != size['nlev']:
                raise IOError('Unrecognized line format')
            d[name]['$data'][i, :, res[0]] = res[1]
        else:
            if dtype == 'float64':
                res = parse_float(rec)
            elif dtype == 'int64':
                res = parse_int(rec)
            else:
                raise AssertionError('Invalid dtype %s' % dtype)
            if len(res) != size['nlev']:
                raise IOError('Unrecognized line format')
            d[name]['$data'][i, :] = res

    elif line.startswith('C:') or line.startswith('R:'):
        pass

    else:
        raise IOError('Unrecognized line format')

    return {
        'i': i,
        'file_level': file_level,
        'level': level,
    }

def mrr2c(f, warning=lambda: None):
    size = parse_size(f)
    f.seek(0)

    d = dataset_template(size)

    fields = {
        v['$attributes']['symbol']: {
            'name': k,
            'dtype': v['$data'].dtype,
            'spectral': len(v['$data'].shape) == 3
        }
        for k, v in d.items()
        if py_.has(v, '$attributes.symbol')
    }

    file_level = None
    level = None

    status = {
        'i': None,
        'file_level': None,
        'level': None
    }
    for line_number, line in enumerate(f.readlines()):
        try:
            status = parse_line(
                py_.trim_end(line, '\r\n'),
                d,
                size,
                fields,
                status
            )
        except Exception as e:
            try:
                raise IOError, 'Error parsing line %d: %s' % (
                    line_number + 1,
                    unicode(e)
                ), sys.exc_info()[2]
            except Exception as e:
                warning(e)

    names = FIELDS.get(status['file_level'], [])
    return py_.pick(d, names)

def main_(infile, outfile, debug=False):
    try:
        with open(infile) as f:
            def warning(s):
                logging.warning('%s: %s' % (infile, unicode(s)))
            d = mrr2c(f, warning=warning)
            jdf.to_hdf(d, outfile)
    except Exception as e:
        errstr = '%s: %s' % (
            infile,
            getattr(e, 'strerror', unicode(e))
        )
        if not debug:
            logging.error(errstr)
        else:
            raise IOError, errstr, sys.exc_info()[2]
    except KeyboardInterrupt:
        pass

def main():
    parser = argparse.ArgumentParser(description='Convert Metek MRR-2 data files to HDF5')
    parser.add_argument('--debug', action='store_true', help='enable debugging')
    parser.add_argument('infile', help='input file')
    parser.add_argument('outfile', help='output file')
    args = parser.parse_args()

    main_(args.infile, args.outfile, debug=args.debug)

if __name__ == '__main__':
    main()
