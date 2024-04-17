import pickle
import numpy as np
from major_project import *

if __name__ == '__main__':
    size_of_m1 = 20
    divisor_power = 90
    m, _ = generate_set(10**divisor_power)
    m = np.array(m)
    with open(f'results_left_size_{size_of_m1}_divisor_{divisor_power}.pkl', "rb") as fp:
        results = pickle.load(fp)
        print(np.dot(m, results['binary_string']))
