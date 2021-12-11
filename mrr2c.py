import signal
signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))

import sys
import argparse
import re
import logging
import traceback as tb
import datetime as dt
import pydash as py_
import numpy as np
import ds_format as ds
import aquarius_time as aq

__version__ = '2.1.0'

NA_INT64 = -9223372036854775808

FORMAT = {
	'MRR_RAW': re.compile(r'^MRR +(?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d) +(?P<time_zone>[^ ]+) +DVS +(?P<DVS>[^ ]+) +DSN +(?P<DSN>[^ ]+) +BW +(?P<BW>[^ ]+) +CC +(?P<CC>[^ ]+) +MDQ +(?P<MDQ1>[^ ]+) +(?P<MDQ2>[^ ]+) +(?P<MDQ3>[^ ]+) +TYP (?P<TYP>RAW)\s*$'),
	'MRR_AVE': re.compile(r'^MRR +(?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d) +(?P<time_zone>[^ ]+) +AVE +(?P<AVE>[^ ]+) +STP +(?P<STP>[^ ]+) +ASL +(?P<ASL>[^ ]+) +SMP +(?P<SMP>[^ ]+) +SVS +(?P<SVS>[^ ]+) +DVS +(?P<DVS>[^ ]+) +DSN +(?P<DSN>[^ ]+) +CC +(?P<CC>[^ ]+) +MDQ +(?P<MDQ1>[^ ]+) +TYP +(?P<TYP>AVE)\s*$'),
	'MRR_PRO': re.compile(r'^MRR +(?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d) +(?P<time_zone>[^ ]+) +AVE +(?P<AVE>[^ ]+) +STP +(?P<STP>[^ ]+) +ASL +(?P<ASL>[^ ]+) +SMP +(?P<SMP>[^ ]+) +SVS +(?P<SVS>[^ ]+) +DVS +(?P<DVS>[^ ]+) +DSN +(?P<DSN>[^ ]+) +CC +(?P<CC>[^ ]+) +MDQ +(?P<MDQ1>[^ ]+) +TYP +(?P<TYP>PRO)\s*$'),
}

META = {
	'time': {
		'.dims': ['time'],
		'long_name': 'time',
		'units': 'days since -4713-11-24 12:00 UTC',
		'calendar': 'proleptic_gregorian',
	},
	'level': {
		'.dims': ['level'],
		'.dtype': 'int64',
		'long_name': 'level number',
		'units': 1,
	},
	'band': {
		'.dims': ['band'],
		'.dtype': 'int64',
		'long_name': 'band number',
		'units': 1,
	},
	'time_zone': {
		'.dims': ['time'],
		'.dtype': 'S8',
		'long_name': 'time zone',
	},
	'height': {
		'.dims': ['time', 'level'],
		'long_name': 'height',
		'units': 'm',
		'symbol': 'H',
	},
	'transfer_function': {
		'.dims': ['time', 'level'],
		'long_name': 'transfer function',
		'symbol': 'TF',
	},
	'spectral_reflectivity': {
		'.dims': ['time', 'level', 'band'],
		'long_name': 'spectral reflectivity',
		'units': 'dB',
		'symbol': 'F',
	},
	'drop_size': {
		'.dims': ['time', 'level', 'band'],
		'long_name': 'drop size',
		'units': 'mm',
		'symbol': 'D',
	},
	'spectral_drop_density': {
		'.dims': ['time', 'level', 'band'],
		'long_name': 'spectral drop density',
		'units': 'm-3 mm-1',
		'symbol': 'N',
	},
	'path_integrated_attenuation': {
		'.dims': ['time', 'level'],
		'long_name': 'path integrated attenuation',
		'units': 'dB',
		'symbol': 'PIA',
	},
	'radar_reflectivity': {
		'.dims': ['time', 'level'],
		'long_name': 'radar reflectivity',
		'units': 'dBZ',
		'symbol': 'Z',
	},
	'attenuated_radar_reflectivity': {
		'.dims': ['time', 'level'],
		'long_name': 'attenuated radar reflectivity',
		'units': 'dBZ',
		'symbol': 'z',
	},
	'rain_rate': {
		'.dims': ['time', 'level'],
		'long_name': 'rain rate',
		'units': 'mm h-1',
		'symbol': 'RR',
	},
	'liquid_water_content': {
		'.dims': ['time', 'level'],
		'long_name': 'liquid water content',
		'units': 'g m-3',
		'symbol': 'LWC',
	},
	'fall_velocity': {
		'.dims': ['time', 'level'],
		'long_name': 'fall velocity',
		'units': 'm s-1',
		'symbol': 'W',
	},
	'calibration_constant': {
		'.dims': ['time'],
		'long_name': 'calibration constant',
		'symbol': 'CC',
	},
	'bandwidth': {
		'.dims': ['time'],
		'long_name': 'bandwidth',
		'symbol': 'BW',
	},
	'valid_spectra_percentage': {
		'.dims': ['time'],
		'long_name': 'percentage of valid spectra',
		'units': 'percent',
		'symbol': 'MDQ1',
	},
	'valid_spectra': {
		'.dims': ['time'],
		'.dtype': 'int64',
		'long_name': 'number of valid spectra',
		'symbol': 'MDQ2',
		'units': '1',
	},
	'total_spectra': {
		'.dims': ['time'],
		'.dtype': 'int64',
		'long_name': 'number of total spectra',
		'symbol': 'MDQ3',
		'units': '1',
	},
	'firmware_version': {
		'.dims': ['time'],
		'.dtype': 'S16',
		'long_name': 'firmware version',
		'symbol': 'DVS',
	},
	'service_version': {
		'.dims': ['time'],
		'.dtype': 'S16',
		'long_name': 'service version',
		'symbol': 'SVS',
	},
	'device_serial_number': {
		'.dims': ['time'],
		'.dtype': 'S16',
		'long_name': 'device serial number',
		'symbol': 'DSN',
	},
	'averaging_time': {
		'.dims': ['time'],
		'long_name': 'averaging time',
		'units': 's',
		'symbol': 'AVE',
	},
	'height_resolution': {
		'.dims': ['time'],
		'long_name': 'height resolution',
		'units': 'm',
		'symbol': 'STP',
	},
	'radar_altitude': {
		'.dims': ['time'],
		'long_name': 'radar altitude above sea level',
		'units': 'm',
		'symbol': 'ASL',
	},
	'sampling_rate': {
		'.dims': ['time'],
		'long_name': 'sampling rate',
		'units': 'Hz',
		'symbol': 'SMP',
	},
	'processing_level': {
		'.dims': ['time'],
		'.dtype': 'S3',
		'long_name': 'processing level',
		'symbol': 'TYP',
	}
}

for v in META.values():
	if '.dtype' in v and v['.dtype'].startswith('S'):
		continue
	elif '.dtype' in v and v['.dtype'] == 'int64':
		v['_FillValue'] = v['missing_value'] = NA_INT64
	else: # float64
		v['_FillValue'] = v['missing_value'] = np.nan

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

def sdecode(x):
	return x if (sys.version_info[0] == 2 or type(x) is not bytes) \
		else x.decode('ascii', errors='ignore')

def parse_mrr(s):
	for k, v in list(FORMAT.items()):
		m = v.match(s)
		if m is not None:
			d = m.groupdict()
			return {
				k1: MRR_TYPES.get(k1, str)(v1)
				for k1, v1 in list(d.items())
			}
	return None

def parse_int(rec):
	return np.array([
		int(x) if x != '' else NA_INT64
		for x in rec[1:]
	])

def parse_float(rec):
	return np.array([
		float(x) if x != '' else np.nan
		for x in rec[1:]
	])

def parse_spectral_float(rec):
	return [
		int(rec[0][1:]),
		np.array([
			float(x) if x != '' else np.nan
			for x in rec[1:]]
		)
	]

def parse_size(f):
	s = {
		'nprofiles': 0,
		'nlevels': 0,
		'nbands': 64,
	}

	def parse_line2(line, s):
		if line.startswith('MRR'):
			s['nprofiles'] += 1
		if line.startswith('H'):
			s['nlevels'] = max(s['nlevels'], len(py_.split(py_.drop(line, 3))))

	for line_number, line in enumerate(f.readlines()):
		try:
			parse_line2(sdecode(line), s)
		except Exception as e:
			raise IOError('Error on line %d: %s' % (
				line_number + 1,
				str(e)
			)).with_traceback(sys.exc_info()[2])
	return s

def parse_line(line, d, s, fields, status):
	i = status['i']
	file_level = status['file_level']
	level = status['level']

	symbols = list(fields.keys())

	field_width = max(1, int((len(line) - 3)/s['nlevels']))
	rec = py_.concat(
		py_.trim(py_.take(line, 3)),
		py_.map_(py_.chunk(py_.drop(line, 3), field_width), lambda x: py_.trim(x))
	)

	sym = rec[0]

	if sym == 'MRR':
		i = i + 1 if i is not None else 0
		res = parse_mrr(line)

		if res is None:
			raise IOError('Unrecognized line format')

		level = res['TYP']
		if file_level is not None and level != file_level:
			raise IOError('Mixed processing levels')
		else:
			file_level = res['TYP']

		if 'time' not in d:
			d['time'] = np.full(s['nprofiles'], np.nan, np.float64)
		if 'time_zone' not in d:
			d['time_zone'] = np.zeros(s['nprofiles'], dtype='S8')

		d['time'][i] = aq.from_date([
			1,
			2000 + res['year'],
			res['month'],
			res['day'],
			res['hour'],
			res['minute'],
			res['second']
		])
		d['time_zone'][i] = res['time_zone']
		for k, v in list(res.items()):
			if k in symbols:
				field = fields[k]
				name = field['name']
				if name not in d:
					d[name] = np.full(s['nprofiles'], np.nan, field['dtype'])
				d[name][i] = v
	elif sym in symbols or py_.nth(sym, 0) in symbols:
		if i is None or file_level is None:
			raise IOError('Missing MRR header')

		if file_level is not None and level != file_level:
			raise IOError('Mixed processing levels')

		if sym in symbols:
			field = fields[sym]
		else:
			field = fields[py_.nth(sym, 0)]
		name = field['name']

		dtype = field['dtype']
		if field['spectral']:
			if dtype == 'float64':
				j, res = parse_spectral_float(rec)
			else:
				raise AssertionError('Invalid dtype %s' % dtype)
			if len(res) != s['nlevels']:
				raise IOError('Unrecognized line format')
			if name not in d:
				d[name] = np.full(
					(s['nprofiles'], s['nlevels'], s['nbands']),
					np.nan,
					dtype
				)
			d[name][i,:,j] = res
		else:
			if dtype == 'float64':
				res = parse_float(rec)
			elif dtype == 'int64':
				res = parse_int(rec)
			else:
				raise AssertionError('Invalid dtype %s' % dtype)
			if len(res) != s['nlevels']:
				raise IOError('Unrecognized line format')
			if name not in d:
				d[name] = np.full(
					(s['nprofiles'], s['nlevels']),
					np.nan,
					dtype
				)
			d[name][i,:] = res

	elif line.startswith('C:') or line.startswith('R:'):
		pass
	else:
		raise IOError('Unrecognized line format')

	status['i'] = i
	status['file_level'] = file_level
	status['level'] = level
	return d

def mrr2c(f, warning=lambda: None):
	s = parse_size(f)
	f.seek(0)

	d = {}
	d['.'] = META

	d['.']['.'] = {
		'software': 'mrr2c (https://github.com/peterkuma/mrr2c)',
		'version': __version__,
		'created': dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
	}

	d['level'] = np.arange(s['nlevels'], dtype=np.int64)
	d['band'] = np.arange(s['nbands'], dtype=np.int64)

	fields = {
		v['symbol']: {
			'name': k,
			'dtype': v.get('.dtype', 'float64'),
			'spectral': len(v['.dims']) == 3,
		}
		for k, v in list(META.items())
		if 'symbol' in v
	}

	status = {
		'i': None,
		'file_level': None,
		'level': None
	}

	for line_number, line in enumerate(f.readlines()):
		try:
			d = parse_line(
				sdecode(line.rstrip(b'\r\n')),
				d,
				s,
				fields,
				status
			)
		except Exception as e:
			warning('Error on line %d: %s' % (
				line_number + 1,
				str(e)
			), sys.exc_info())
	return d

def main_(input_, output, debug=False):
	try:
		with open(input_, 'rb') as f:
			def warning(s, exc_info):
				msg = '%s: %s' % (input_, s)
				if not debug:
					logging.warning(msg + ' (use --debug for more information)')
				else:
					logging.warning(msg)
					tb.print_exception(*exc_info)
			d = mrr2c(f, warning=warning)
			ds.write(output, d)
	except Exception as e:
		msg = '%s: %s' % (
			input_,
			str(e),
		)
		if not debug:
			logging.error(msg + ' (use --debug for more information)')
		else:
			raise IOError(msg).with_traceback(sys.exc_info()[2])

def main():
	parser = argparse.ArgumentParser(description='Convert Metek MRR-2 data files to NetCDF')
	parser.add_argument('--debug', action='store_true', help='enable debugging')
	parser.add_argument('input', help='input file')
	parser.add_argument('output', help='output file')
	args = parser.parse_args()
	main_(args.input, args.output, debug=args.debug)

if __name__ == '__main__':
	main()
