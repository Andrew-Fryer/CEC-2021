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
    cur = np.array(power_usage.iloc[i])
    power = 0
    renewables = 0
    cost = 0
    ppr_copy = 1000*ppr.copy()
    #Use local power first
    for j in range(len(cur)):
        index = 4
        while (index >= 0 and cur[j] > 0 and ppr_copy[j][index] >= 0):
            change = min(cur[j], ppr_copy[j][index])
            cur[j] -= change
            ppr_copy[j][index] -= change
            power += change
            if (index >= 3):
                renewables += change
            emitters = 0
            if (index < 2):
                emitters += change
            nonemitters = 0
            if (index >= 2):
                nonemitters += change
            cost += penalties[j][j]*change + emitters*emission_tax + nonemitters*non_emission_tax
            index -= 1
    
    #Deal with zones who didnt have enough power
    need_power = []
    for j in range(len(cur)):
        if cur[j] > 0:
            need_power.append(j)
    
    for j in range(len(cur)):
        if j in need_power:
            count = 0
            for k in ppr_copy:
                index = 4
                while (index >= 0 and cur[j] > 0 and k[index] >= 0):
                    change = min(cur[j], k[index])
                    cur[j] -= change
                    k[index] -= change
                    power += change
                    if (index >= 3):
                        renewables += change
                    emitters = 0
                    if (index < 2):
                        emitters += change
                    nonemitters = 0
                    if (index >= 2):
                        nonemitters += change
                    cost += penalties[count][j]*change + emitters*emission_tax + nonemitters*non_emission_tax
                    index -= 1
                if (cur[j] <= 0):
                    break
                count += 1
            
    #Release extra renewables
    count = 0
    for j in ppr_copy:
        for k in range(2, 5):
            if (j[k] > 0):
                best = 1
                best_i = -1
                for l in range(7, 11):
                    if (penalties[l][count] < best):
                        best = penalties[l][count]
                        best_i = l
                change = j[k]
                j[k] -= change
                if k > 2:
                    renewables += change
                power += change
                cost += penalties[l][count]*change - change*non_emission_tax
        count += 1
            
    power = power/1000000
    renewables = renewables/1000000
    out.append([cost, power, renewables/power])
    

# out = []
# for i in range(12):
#     cur = Pn[i]
#     extra = []
#     need = []
#     count = 0
#     for j in cur:
#         if (j < 0):
#             extra.append(j)
#         else:
#             need.append({'name': count, 'best': []})
#             extra.append(0)
#         count += 1
    
#     for l in need:
#         for j in range(len(extra)):
#             if (extra[j] < 0):
#                 l['best'].append({'name': j, 'penalty': penalties[j][l['name']]})
#         l['best'] = sorted(l['best'], key=lambda x: x['penalty'], reverse=False)
        
#     cost = 0
#     power = 0
#     renewables = 0
#     for j in range(len(extra)):
#         if extra[j] < 0:
#             power += power_usage.iloc[i][j]
#             cost += penalties[j][j]*power_usage.iloc[i][j] + emission_tax*Pg[j,2] - non_emission_tax*Pg[j,3]
#             renewables += Pg[j,0]
    
#     for l in need:
#         index = 0
#         while index < len(l['best']) and cur[l['name']] < 0:
#             change = min(-cur[l['name']], extra[l['best'][index]['name']])
#             extra[l['best'][index]['name']] -= change
#             cur[l['name']] += change
#             cost += penalties[l['best'][index]['name']][l['name']]*change
#             power += change
#             index += 1
    
#     power = power/1000000
#     renewables = renewables/1000000
    
#     out.append([cost, power, renewables/power])
# out = np.array(out)