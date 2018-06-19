import numpy as np
import re

def retrieve_lat_lon(filename):
    with open(filename) as f:
        match = re.match(r'^lat0 (.*), lon0 (.*)$', f.readline())
        if match:
            return np.fromstring(f'{match.group(1)},{match.group(2)}', dtype='Float64', sep=',')
    return float('37.792480'), float('-122.397450') # Could have handled mis match criteria but currently am using this as a placeholder.
