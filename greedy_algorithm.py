import emission_tax, non_emission_tax, penalty_values, plant_production_rates, nb_zones, total_zones from parse



def dot_product(v1, v2):
    assert(len(v1) == len(v2))

    return sum([[x*y for x in v1] for y in v2])

def cost(zone_penalty_vector, zone_power_vector, emissive_power, non_emissive_power):
    return dot_product(zone_penalty_vector, zone_power_vector) + emission_tax * emissive_power - non_emission_tax * non_emissive_power

def get_zone_penalty_vector(zone):
    assert(zone in total_zones)

    return penalty_values[zone]

demands = [] # from Farley

demand_df = penalty_values.copy(deep=True)
demand_df.insert(loc=1, column='demand', value=demands)
for zone in nb_zones:
    demand_df.insert(column=zone + '_usage', value=0)

for energy_type in ['nuclear', 'hydro', 'wind']:
    demand_df.insert(column=energy_type, value=-emission_tax)
    demand_df.insert(column=energy_type + '_usage', value=0)

for energy_type in ['thermal', 'combustion']:
    demand_df.insert(column=energy_type, value=non_emission_tax)
    demand_df.insert(column=energy_type + '_usage', value=0)

    

'''
    zone, demand, z0_penalty, z0_usage, z1_penalty, z1_usage, ... hydro_penalty, hydro_usage, cost_function
'''


def greedy_algorithm():
    for zone in nb_zones:
        demand = something
        cost = 0
        # Since using non-emissive power sources is always negative cost (and nothing else is),
        # we should use them as much as possible
        usages = []
        for energy_type in ['nuclear', 'hydro', 'wind']:
            supply = plant_production_rates.something
            usage = min(demand, supply)
            usages.append((energy_type, usage))
            demand -= usage
            cost -= non_emission_tax * usage + zone_penalty_vector[zone] * usage
        
        zone_penalty_vector = penalty_values.something # tuples of source names and penalties?
        # the cost function is the same if we add the emissive cost to the 
        zone_penalty_vector[zone] += emission_tax

        # greedily take power
        zone_penalty_vector.sort()
        for source in zone_penalty_vector:
            supply = something
            usage = min(demand, suplly)
            demand -= usage
            cost += something

