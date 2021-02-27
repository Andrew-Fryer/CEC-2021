import pandas as pd

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

nb_zones = ['z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']
total_zones = nb_zones.copy() + ['z8', 'z9', 'z10', 'z11']

energy_types = ['thermal', 'nuclear', 'combustion', 'hydro', 'wind']

incentive_rates = pd.read_csv('Information/IncentiveRates.csv', header=None)
[emission_tax, non_emission_tax] = incentive_rates.values[0]
# incentive_rates are already in kWh

plant_production_rates = pd.read_csv('Information/PlantProductionRates.csv', names=energy_types.copy())
plant_production_rates.insert(loc=0, column='zone', value=nb_zones.copy())
# normalize values from MW to kW
for e_type in energy_types:
    plant_production_rates[e_type] = plant_production_rates[e_type] * 1000
# plant_production_rates are now all in kW

penalty_values = pd.read_csv('Information/PenaltyValues.csv', header=None, names=total_zones.copy())
penalty_values.insert(loc=0, column='zone', value=total_zones.copy())
# penalty_values are already in $/kWh

trend_2015 = pd.read_csv('PastYearData/NBTrend2015.csv', header=None, names=nb_zones.copy())
trend_2015.insert(loc=0, column='months', value=months.copy())

trend_2016 = pd.read_csv('PastYearData/NBTrend2016.csv', header=None, names=nb_zones.copy())
trend_2016.insert(loc=0, column='months', value=months.copy())

trend_2017 = pd.read_csv('PastYearData/NBTrend2017.csv', header=None, names=nb_zones.copy())
trend_2017.insert(loc=0, column='months', value=months.copy())

trend_2018 = pd.read_csv('PastYearData/NBTrend2018.csv', header=None, names=nb_zones.copy())
trend_2018.insert(loc=0, column='months', value=months.copy())

# normalize all trend data from GWh to kWh
for df in [trend_2015, trend_2016, trend_2017, trend_2018]:
    for zone in nb_zones:
        df[zone] = df[zone] * 1000000
# all trend data is now in kWh

pass