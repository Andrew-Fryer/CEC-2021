from parse import emission_tax, non_emission_tax, penalty_values, plant_production_rates, nb_zones, total_zones
from power_consumption_predict import *
from clean_energy_types import *

def get_penalty_factor(current_zone_index, energy_type, other_zone):
    assert(energy_type in energy_types)
    transmission_cost = penalty_values[other_zone][zone_index]
    if(is_non_emissive(energy_type)):
        return transmission_cost - non_emission_tax
    else:
        return transmission_cost + emission_tax

predicted_power_usage = get_predicted_power_usage(2019)
demands = list(predicted_power_usage.loc[0])

supply_df = plant_production_rates.copy(deep=True).set_index('zone').unstack()
supply_dict = supply_df.T.to_dict()
supply_left_dict = {}
for t in supply_dict:
    supply_left_dict[t] = supply_dict[t]


# Ensure that each zone gets enough power
cost = 0
usages = {}
for zone_index in range(len(nb_zones)):
    demand = demands[zone_index]

    sources = [(t, get_penalty_factor(zone_index, t[0], t[1])) for t in supply_dict]

    sources = sorted(sources, key=lambda t: t[1])

    for source in sources:
        if(demand == 0):
            break
        t, penalty_factor = source
        energy_type, zone = t
        usage = min(demand, supply_left_dict[t])
        if(usage > 0):
            usages[(zone_index, zone, energy_type)] = usage
        supply_left_dict[t] -= usage
        demand -= usage
        cost += penalty_factor * usage
    assert(demand == 0)
