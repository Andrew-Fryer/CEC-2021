from parse import *
import numpy as np
from power_consumption_predict import *

'''
algorithm:
    The main algorithm to optimize NB energy demands.
    
    year - The year to analyze
    
    output - The requested output returned in a pandas dataframe
'''
@track_memory_use(close=False, return_history=False, plot=True)
def algorithm(year):
    #Load and process neccessary data
    power_usage = get_predicted_power_usage(year)
    
    penalties = np.array(penalty_values.iloc[0:, 1:])
    ppr = np.array(plant_production_rates.iloc[0:, 1:])
    
    #Loop over every month and calculate total cost, power consumption, and renewables
    output = []
    for i in range(12):
        demand_for_current_month = np.array(power_usage[0].iloc[i])
        power = 0
        renewables = 0
        cost = 0
        ppr_copy = ppr.copy()
        #Use local power first
        for j in range(len(demand_for_current_month)):
            energy_index = 4
            #Loop through all energy sources, trying to use renewables first
            while (energy_index >= 0 and demand_for_current_month[j] > 0 and ppr_copy[j][energy_index] >= 0): 
                change = min(demand_for_current_month[j], ppr_copy[j][energy_index])
                #Decrement needed and used power
                demand_for_current_month[j] -= change
                ppr_copy[j][energy_index] -= change
                power += change
                #Add values where approriate
                if (energy_index >= 3):
                    renewables += change
                emitters = 0
                if (energy_index == 0 or energy_index == 2):
                    emitters += change
                nonemitters = 0
                if (energy_index == 1 or energy_index >= 3):
                    nonemitters += change
                #Update cost
                cost += penalties[j][j]*change + emitters*emission_tax - nonemitters*non_emission_tax
                energy_index -= 1
        
        #Deal with zones who didnt have enough power
        need_power = []
        #Find zones that need power
        for j in range(len(demand_for_current_month)):
            if demand_for_current_month[j] > 0:
                need_power.append(j)
        for j in need_power:
            #Loop through zones with excess power, saving the lowest cost
            count = 0
            best_i = -1
            best = 10000000000000
            power_best = 0
            renewable_best = 0
            for k in ppr_copy:
                energy_index = 4
                while (energy_index >= 0 and demand_for_current_month[j] > 0 and k[energy_index] >= 0):
                    change = min(demand_for_current_month[j], k[energy_index])
                    #Add values where approriate
                    emitters = 0
                    if (energy_index == 0 or energy_index == 2):
                        emitters += change
                    nonemitters = 0
                    if (energy_index == 1 or energy_index >= 3):
                        nonemitters += change
                    cost_change = penalties[count][j]*change + emitters*emission_tax - nonemitters*non_emission_tax
                    if cost_change < best:
                        best_i = energy_index
                        best = cost_change
                        power_best = change
                        if energy_index >= 3:
                            renewable_best = change
                    energy_index -= 1
                count += 1
            if (best_i >= 0):
                cost += best
                power += power_best
                renewables += renewable_best
                demand_for_current_month[j] -= power_best
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
        output.append([cost, power, 100*renewables/power])
        
    return pd.DataFrame(output)



if __name__ == "__main__":
    algorithm(2022)

