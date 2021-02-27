from parse import *
import numpy as np
from power_consumption_predict import *

CUR_YEAR = 2019

def get_class_mat():
    return np.array([[0, 1, 1, 0],
                     [0, 1, 0, 1],
                     [0, 1, 1, 0],
                     [1, 0, 0, 1],
                     [1, 0, 0, 1]])

power_usage = get_predicted_power_usage(CUR_YEAR)

penalties = np.array(penalty_values.iloc[0:, 1:])
ppr = np.array(plant_production_rates.iloc[0:, 1:])

Pg = np.dot(ppr, get_class_mat())
Pn = []
for i in range(12):
    tmp = []
    for j in range(7):
        tmp.append(power_usage.iloc[i][j] - 1000*sum(Pg[j]))
    Pn.append(tmp)
Pn = np.array(Pn)

out = []
for i in range(12):
    cur = Pn[i]
    extra = []
    need = []
    count = 0
    for j in cur:
        if (j < 0):
            extra.append(j)
        else:
            need.append({'name': count, 'best': []})
            extra.append(0)
        count += 1
    
    for l in need:
        for j in range(len(extra)):
            if (extra[j] < 0):
                l['best'].append({'name': j, 'penalty': penalties[j][l['name']]})
        l['best'] = sorted(l['best'], key=lambda x: x['penalty'], reverse=False)
        
    cost = 0
    power = 0
    renewables = 0
    for j in range(len(extra)):
        if extra[j] < 0:
            power += power_usage.iloc[i][j]
            cost += penalties[j][j]*power_usage.iloc[i][j] + emission_tax*Pg[j,2] - non_emission_tax*Pg[j,3]
            renewables += Pg[j,3]
    
    for l in need:
        index = 0
        while index < len(l['best']) and cur[l['name']] < 0:
            change = min(-cur[l['name']], extra[l['best'][index]['name']])
            extra[l['best'][index]['name']] -= change
            cur[l['name']] += change
            cost += penalties[l['best'][index]['name']][l['name']]*change
            power += change
            index += 1
    
    out.append([cost, power, renewables/power])
out = np.array(out)