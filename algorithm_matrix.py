from parse import *
import numpy as np
import scipy
from scipy import linalg, matrix

def null(A, eps=1e-15):
    u, s, vh = scipy.linalg.svd(A)
    null_mask = (s <= eps)
    null_space = scipy.compress(null_mask, vh, axis=0)
    return scipy.transpose(null_space)

def get_optimal_values(penalty_values, non_emission_tax, emission_tax, zone):
    AMat = []
    for i in range(len(penalty_values)):
        cur = []
        for j in range(len(penalty_values)+1):
            if (i == j or j == len(penalty_values)):
                cur.append(penalty_values.iloc[i, zone+1])
            else:
                cur.append(0)
        AMat.append(cur)
    for i in range(len(penalty_values)):
        cur = [0 for j in range(len(penalty_values))]
        cur.append(emission_tax)
        AMat.append(cur)
    cur = [-non_emission_tax for j in range(len(penalty_values))]
    cur.append(0)
    AMat.append(cur)
    
    AMat = matrix(AMat)
    
    X = AMat * null(AMat)
    
    return X

tmp = get_optimal_values(penalty_values, non_emission_tax, emission_tax, 0)