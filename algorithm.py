from parse import *
import numpy as np
from power_consumption_predict import *

def algorithm(year):
    power_usage = get_predicted_power_usage(year)
    
    penalties = np.array(penalty_values.iloc[0:, 1:])
    ppr = np.array(plant_production_rates.iloc[0:, 1:])
    
    out = []
    for i in range(12):
        cur = np.array(power_usage[0].iloc[i])
        power = 0
        renewables = 0
        cost = 0
        ppr_copy = ppr.copy()
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
                best_i = -1
                best = 10000000000000
                power_best = 0
                renewable_best = 0
                for k in ppr_copy:
                    index = 4
                    while (index >= 0 and cur[j] > 0 and k[index] >= 0):
                        change = min(cur[j], k[index])
                        cost_change = penalties[count][j]*change + emitters*emission_tax + nonemitters*non_emission_tax
                        if cost_change < best:
                            best_i = index
                            best = cost_change
                            power_best = change
                            if index >= 3:
                                renewable_best = change
                        index -= 1
                    count += 1
                if (best_i >= 0):
                    cost += best
                    power += power_best
                    renewables += renewable_best
                    cur[j] -= power_best
                    ppr_copy[j][best_i] -= power_best
                
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
        
    return pd.DataFrame(out)