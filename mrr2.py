#!/usr/bin/python

import sys
import pydash as py_
import re
import numpy as np
import jdf
from jdf.na import *
import logging
import fortranformat as ff

TIME_RE = re.compile('(?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d)')

FORMAT = {
    'mrr_ave': re.compile('MRR (?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d) (?P<time_zone>.{3}) AVE (?P<AVE>.{5}) STP (?P<STP>.{5}) ASL (?P<ASL>.{5}) SMP (?P<SMP>.{5}) SVS (?P<SVS>.{7}) DVS (?P<DVS>.{4}) DSN (?P<DSN>.{10}) CC (?P<CC>.{7}) MDQ (?P<MDQ>.{3}) TYP (?P<TYP>.{3})')
}

# def parse_time(s):
#     m = TIME_RE.match(s)
#     print(s)
#     res = {k: int(v) for k, v in m.groupdict().iteritems()}
#     return '20%(year)02d-%(month)02d-%(day)02dT%(hour)02d:%(minute)02d:%(second)02d' % (
#         res
#     )

def format_time(year, month, day, hour, minute, second):
    return '20%(year)02d-%(month)02d-%(day)02dT%(hour)02d:%(minute)02d:%(second)02d' % locals()

def parse_mrr(s):
    for k, v in FORMAT.items():
        # reader = ff.FortranRecordReader(v['format'])
        # res = reader.read(s)
        # res = scanf(v['format'], s, False)
        # print(s, res)
        m = v.match(s)
        if m is not None:
            return m.groupdict()
            # return {
            #     x: y
            #     for x, y in zip(v['args'], res)
            # }
    return None

# def parse_mrr(rec):
#     print(rec)
#     d = {
#         'time': parse_time(rec[1]),
#         'time_zone': rec[2],
#     }

#     i = 3
#     while i < len(rec):
#         k = rec[i]
#         if k == 'DVS':
#             d[k] = py_.nth(rec, i + 1)
#             i += 1
#         elif k == 'DSN':
#             d[k] = py_.nth(rec, i + 1)
#             i += 1
#         elif k == 'BW':
#             d[k] = float(py_.nth(rec, i + 1))
#             i += 1
#         elif k == 'CC':
#             d[k] = float(py_.nth(rec, i + 1))
#             i += 1
#         elif k == 'MDQ':
#             d[k] = [
#                 int(py_.nth(rec, i + 1)),
#                 int(py_.nth(rec, i + 2)),
#                 int(py_.nth(rec, i + 3))
#             ]
#             i += 3
#         elif k == 'TYP':
#             d[k] = py_.nth(rec, i + 1)
#             i += 1
#         elif k == 'AVG':
#             d[k] = py_.nth(rec, i + 1)
#             i += 1
#         i += 1

#     return d

def parse_int(rec):
    return np.array([int(x) for x in rec[1:]])

def parse_float(rec):
    return np.array([float(x) for x in rec[1:]])

def parse_spectral_float(rec):
    return [
        int(rec[0][1:]),
        np.array([float(x) for x in rec[1:]])
    ]

def parse_size(f):
    d = {
        'nprof': 0,
        'nlev': 32,
        'nspectral': 64,
    }

    def parse_line(line, d):
        if line.startswith('MRR'):
            d['nprof'] += 1

    for line_number, line in enumerate(f.readlines()):
        try:
            parse_line(line, d)
        except Exception as e:
            raise IOError, 'Error parsing line %d: %s' % (
                line_number,
                unicode(e)
            ), sys.exc_info()[2]

    return d

def parse(file):
    with open(file) as f:
        size = parse_size(f)
        f.seek(0)

        d = {
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
                    'units': 'm'
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
                    'units': 'percent'
                }
            },
            'valid_spectra': {
                '$data': NA_INT64*np.ones(size['nprof'], 'int64'),
                '$attributes': {
                    'long_name': 'number of valid spectra'
                }
            },
            'total_spectra': {
                '$data': NA_INT64*np.ones(size['nprof'], 'int64'),
                '$attributes': {
                    'long_name': 'number of total spectra'
                }
            },
            'device_version': {
                '$data': np.zeros(size['nprof'], 'S16'),
                '$attributes': {
                    'long_name': 'device version',
                    'symbol': 'DSV'
                }
            },
            'device_serial_number': {
                '$data': np.zeros(size['nprof'], 'S16'),
                '$attributes': {
                    'long_name': 'device serial number',
                    'symbol': 'DSN'
                }
            }
        }

        fields = {
            v['$attributes']['symbol']: {
                'name': k,
                'dtype': v['$data'].dtype,
                'spectral': len(v['$data'].shape) == 3
            }
            for k, v in d.items()
            if py_.has(v, '$attributes.symbol')
        }

        symbols = fields.keys()

        def parse_line(line, i):
            rec = py_.concat(
                py_.take(line, 3),
                py_.chunk(py_.drop(line, 3), 7)
            )
            if rec[0] == 'MRR':
                i = i + 1 if i is not None else 0
                res = parse_mrr(line)
                if res is None:
                    raise IOError('Failed to parse MRR line')
                d['time']['$data'][i] = format_time(
                    int(res['year']),
                    int(res['month']),
                    int(res['day']),
                    int(res['hour']),
                    int(res['minute']),
                    int(res['second']),
                )
                d['time_zone']['$data'][i] = res['time_zone']
                d['calibration_constant']['$data'][i] = float(res['CC'])
                d['device_version']['$data'][i] = res['DVS']
                d['device_serial_number']['$data'][i] = res['DSN']
                d['bandwidth']['$data'][i] = float(res['BW'])
                d['valid_spectra_percentage']['$data'][i] = float(res['MDQ'][0])
                d['valid_spectra']['$data'][i] = int(res['MDQ'][1])
                d['total_spectra']['$data'][i] = int(res['MDQ'][2])
            elif rec[0] in symbols or py_.nth(rec[0], 0) in symbols:
                if rec[0] in symbols:
                    x = fields[rec[0]]
                else:
                    x = fields[py_.nth(rec[0], 0)]
                name = x['name']
                dtype = str(x['dtype'])
                if x['spectral'] is True:
                    if dtype == 'float64':
                        res = parse_spectral_float(rec)
                        d[name]['$data'][i, :, res[0]] = res[1]
                    else:
                        raise AssertionError('Invalid dtype %s' % dtype)
                else:
                    if dtype == 'float64':
                        res = parse_float(rec)
                        d[name]['$data'][i, 0:len(res)]
                    elif dtype == 'int64':
                        res = parse_int(rec)
                        d[name]['$data'][i, 0:len(res)] = res
                    else:
                        raise AssertionError('Invalid dtype %s' % dtype)
            return i

        i = None
        for line_number, line in enumerate(f.readlines()):
            try:
                i = parse_line(line, i)
            except Exception as e:
                raise IOError, 'Error parsing line %d: %s' % (
                    line_number,
                    unicode(e)
                ), sys.exc_info()[2]

        return d

def main(infile, outfile, debug=False):
    try:
        d = parse(infile)
        jdf.to_hdf(d, outfile)
    except Exception as e:
        if not debug:
            logging.error(unicode(e))
        else:
            raise

main(sys.argv[1], sys.argv[2], debug=True)
