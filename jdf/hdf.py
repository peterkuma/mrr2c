from .jdf import JDFArray
from .na import *
import pydash as py_
import h5py
import numpy as np


def convert_attributes(attrs):
    a = {}
    for name in attrs:
        try:
            a[name] = str(attrs[name])
        except:
            pass
    return a


def convert_group(group, file, path=[], **opts):
    d = {}
    d['@attributes'] = convert_attributes(group.attrs)
    for name in group:
        obj = group[name]
        newpath = py_.concat(
            path,
            name
        )
        if isinstance(obj, h5py.Group):
            d[name] = convert_group(obj, file=file, path=newpath, **opts)
        elif isinstance(obj, h5py.Dataset):
            d[name] = convert_dataset(obj, file=file, path=newpath, **opts)
    return d


def convert_dtype(dtype):
    return str(dtype)


def convert_dataset(dataset, file, path=[], **opts):
    f = {}
    f['@attributes'] = convert_attributes(dataset.attrs)
    f['@type'] = convert_dtype(dataset.dtype)
    f['@size'] = dataset.shape

    def convert(data):
        return data

    def read(key):
        with h5py.File(file) as h:
            dataset = py_.get(h, path)
            if f['@size'] == () and key == slice(None):
                data = np.array([dataset[()]])
            else:
                data = dataset[key]
            # print data
            return convert(data)

    f['@data'] = JDFArray(read)
    return f

    # if opts.get('cf_time'):
    #     if dataset.attrs.get('units') == 'iso8601':
    #         d[name] = {
    #             '@data': [dt.datetime.strptime(x.decode('ascii'), '%Y-%m-%dT%H:%M:%S.%fZ') for x in f[name][::]],
    #             '@type': '',
    #         }
    #     else:
    #         def getitem(key):
    #             h5py.File(file)

    #         data = JDFArray(getitem)
    #         d[name] = {
    #             '@data':
    #             '@type': '',
    #         }


def to_hdf(d, file):
    # def group(h, d):
    #     for name, f in d:
    #         if '@data' in f:
    #             field(h, d)
    #         else:
    #             pass
    # def field

    with h5py.File(file, 'w') as h:
        # group(h, d)
        for name, field in d.items():
            if name.startswith('_'):
                continue
            if py_.get(field, '$type') == 'datetime':
                ds = h.create_dataset(
                    name,
                    dtype='S31',
                    data=[jdf_datetime(x) for x in field['$data']]
                )
                ds.attrs['units'] = 'iso8601'
            else:
                dtype = py_.get(field, '$type', field['$data'].dtype)
                ds = h.create_dataset(
                    name,
                    dtype=dtype,
                    data=py_.get(field, '$data')
                )
            for name, value in field['$attributes'].items():
                if (type(value) == str or type(value) == unicode):
                    ds.attrs[name] = np.string_(value)
                else:
                    ds.attrs[name] = value
            missing_value = {
                'float64': NA_FLOAT64,
                'int64': NA_INT64
            }.get(str(dtype))
            if missing_value:
                ds.attrs['missing_value'] = missing_value


def from_hdf(file, **opts):
    d = {}
    with h5py.File(file) as h:
        d = convert_group(h, file=file, **opts)
    return d
