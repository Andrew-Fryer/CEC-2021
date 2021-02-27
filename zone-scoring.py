import * from parse

zone_keys = ["z1", "z2", "z3", "z4", "z5",
             "z6", "z7", "z8", "z9", "z10", "z11"]
zone_costs = dict.fromkey(zone_keys, 0)

# Returns a zone's cost per month
'''
h_zone: kWh -> power sent from external zones -> vector (python list)
p: $/kWh -> penalty for sending power to zone -> vector (python list)
e: $/kWh -> carbon tax (for generated/emissive) -> float
h_emissive: kWh -> total generated in zone (emissive) -> float
b: $/kWh -> bonus for using non-emissive -> float
h_non_emissive: kWh -> total generated in zone (non-emissive) -> float

Equation:
    C_zone,month = p_zone * h_zone + e * h_emissive - b * h_non_emissive
Output:
    $/kWh for the given zone per month
'''


def get_zone_cost(p_zone, h_zone, e, h_emissive, b, h_non_emissive):
    external_zone_power = 0

    for i in len(p_zone):
        external_zone_power += p_zone[i]*h_zone[i]

    return external_zone_power + cost_local_power_production(e, h_emissive, b, h_non_emissive)


# cost of power produced locally
def cost_local_power_production(e, h_emissive, b, h_non_emissive):
    return e*h_emissive - b*h_non_emissive


# Returns a province's cost per month
def total_province_cost():
    total = 0
    for i in len(zone_costs):
        key = "z"+(i+1)
        total += zone_costs[key]


# Meeting power requirements
'''
Input:
predicted_power_demand: how much power is needed for this month in this zone
power_produced_locally: how much power does the province produce locally

Output:
What is the order of using power from provinces + how much from each (depends on the cost)
'''

# What zones are connected to the zone I'm looking in?
# returns of a list of the zones i'm near


def zones_nearby():
    return


def meet_power_requirements(predicted_power_demand, power_produced_locally, e, h_emissive, b, h_non_emissive):
    local_power_cost = cost_local_power_production(
        e, h_emissive, b, h_non_emissive)
    # Can we meet all of the requirments locally?
    if(predicted_power_demand == power_produced_locally):
        # Yes?
        # Check to see if this is the most cost efficient? -> do we want to find a way to further emphasize green energy or are we just looking to save money?
        # -> do this by comparing all of the sending costs (green energy ones that is -> if we can meet it, we don't want to pull non-green resources)

        # Need to be comparing each source individually

        '''
        list_of_sources_in_current_zone = {} -> this dictionary should be key=source, value=cost_of_power
        for loop with results from zones_nearby:
            sources_in_external_zones={}{} -> assign the zone's key1=zone, key2=source, value=cost_of_power

        compare power values with current zone and see if anything improves it (while still meeting the same amount of power)

        return list of dictionaries containing which zone & source to pull from (no two 2d dictionaries in this one) in order of best to worst
        '''

    # No?
    # Check combinations of the power cost with external power
    # Is it cheap to even use the zone's power at all (like say if it's not green)?

    '''
        What zones that are nearby can actually meet our power demands?
        check zone_nearby if they can produce enough power to meet our demand?
        if yes? continue with this list. if no? branch to other zones


    '''
