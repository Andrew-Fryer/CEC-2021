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

supply_df = plant_production_rates.copy(deep=True).set_index('zone').unstack()
supply_dict = supply_df.T.to_dict()
supply = [{'zone': t[0], 'energy_type': t[1], 'supply': supply_dict[t]} for t in supply_dict]

def get_penalty_factor(current_zone_index, energy_type, other_zone):
    assert(energy_type in energy_types)
    #if(energy_type in ['nuclear', 'hydro', 'wind']):
    return penalty_values[other_zone][zone_index]

# for each month:
# First, try to distribute power most efficiently

# Then, ensure that each zone gets enough power
cost = 0
for zone_index in range(len(nb_zones)):
    demand = demand_df['demand'][zone_index]

    sources = [(t, get_penalty_factor(zone_index, t[0], t[1])) for t in supply_dict]

    sources = sorted(sources, key=lambda t: t[1])

    for source in sources:
        t, penalty_factor = source
        energy_type, zone = t
        usage = min(demand, supply_dict[t])
        #demand_df.at[name + '_usage', zone_index] = usage
        demand -= usage
        cost += penalty_factor * usage
    assert(demand == 0)

# Finally, sell any leftover power

pass
