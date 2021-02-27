from parse import emission_tax, non_emission_tax, penalty_values, plant_production_rates, nb_zones, total_zones
from power_consumption_predict import *

predicted_power_usage = get_predicted_power_usage(2019)
demands = list(predicted_power_usage.loc[0])

demand_df = penalty_values.copy(deep=True).head(7)
demand_df.insert(loc=1, column='demand', value=demands)
demand_df['usage'] = demand_df['demand'].copy()
for zone in nb_zones:
    demand_df[zone + '_usage'] = 0

for energy_type in ['nuclear', 'hydro', 'wind']:
    demand_df[energy_type] = -emission_tax
    demand_df[energy_type + '_usage'] = 0

for energy_type in ['thermal', 'combustion']:
    demand_df[energy_type]= non_emission_tax
    demand_df[energy_type + '_usage'] = 0

'''
    zone, demand, z0_penalty, z0_usage, z1_penalty, z1_usage, ... hydro_penalty, hydro_usage, cost_function
'''

# Normalize by environmental incentives
''' this requires having cols for z0_nuclear, z0_hydro, etc...'''
#demand_df[]

supply_df = plant_production_rates.copy(deep=True).set_index('zone').unstack()

# for each month:
# First, try to distribute power most efficiently

# Then, ensure that each zone gets enough power
cost = 0
for zone_index in range(len(nb_zones)):
    demand = demand_df['demand'][zone_index]

    def helper(t):
        energy_type = t[0][0]
        zone = t[0][1]
        penalty_factor = penalty_values[zone][zone_index] # todo account for tax thing
        return (energy_type, zone, t[1], penalty_factor)

    sources = [helper(t) for t in supply_df.T.to_dict().items()]

    sources = sorted(sources, key=lambda t: t[3])

    for source in sources:
        energy_type, zone, supply, penalty_factor = source
        usage = min(demand, supply)
        #demand_df.at[name + '_usage', zone_index] = usage
        demand -= usage
        cost += penalty_factor * usage
    #assert(demand == 0)



    

# Finally, sell any leftover power


