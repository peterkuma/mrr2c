import h5py
import json
import numpy as np
# import datetime as dt

class JDFArray:
    def __init__(self, fun):
        self._fun = fun

    def __getitem__(self, key):
        return self._fun(key)


def to_json(d):
    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, JDFArray):
                return o[::]
            if isinstance(o, np.ndarray):
                if o.ndim == 1:
                    return o.tolist()
                else:
                    return [self.default(o[i]) for i in range(o.shape[0])]
            return json.JSONEncoder.default(self, o)

    return json.dumps(d, cls=JSONEncoder)


# def jdf_datetime(datetime):
#     return datetime.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ').encode('ascii', 'ignore')
