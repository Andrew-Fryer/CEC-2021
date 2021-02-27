from parse import energy_types

def is_non_emissive(energy_type):
    assert(energy_type in energy_types)

    return energy_type in ['nuclear', 'hydro', 'wind']

def is_renewable(energy_type):
    assert(energy_type in energy_types)

    return energy_type in ['hydro', 'wind']
