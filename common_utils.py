import numpy as np
import re

def retrieve_lat_lon(filename):
    with open(filename) as f:
        match = re.match(r'^lat0 (.*), lon0 (.*)$', f.readline())
        if match:
            return np.fromstring(f'{match.group(1)},{match.group(2)}', dtype='Float64', sep=',')
    return float('37.792480'), float('-122.397450') # Could have handled mis match criteria but currently am using this as a placeholder.


def prune(path, epsilon=1e-6):
    
    def point(p):
        return np.array([p[0], p[1], 1.]).reshape(1, -1)

    def collinearity_check(p1, p2, p3):   
        m = np.concatenate((p1, p2, p3), 0)
        det = np.linalg.det(m)
        return abs(det) < epsilon

    pruned_path = [p for p in path]
    i = 0
    while i < len(pruned_path) - 2:
        p1 = point(pruned_path[i])
        p2 = point(pruned_path[i+1])
        p3 = point(pruned_path[i+2])
        collinear = collinearity_check(p1, p2, p3)
        if collinear:
            pruned_path.remove(pruned_path[i+1])
        else:
            i += 1
    return pruned_path