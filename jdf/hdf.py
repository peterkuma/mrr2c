from .na import *
import pydash as py_
import h5py
import numpy as np

def to_hdf(d, file):
    with h5py.File(file, 'w') as h:
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
