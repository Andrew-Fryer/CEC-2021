import pandas as pd

incentive_rates = open('Information/IncentiveRates.csv', 'r').readlines()[0].split(',')
[emission_tax, non_emission_tax] = [0.015, 0.009] # [float(x) for x in incentive_rates]

# penalty_values = [[float(x) for x in y.split(',')] for y in open('Information/PenaltyValues.csv', 'r').readlines()]

penalty_values = pd.read_csv('Information/PenaltyValues.csv', header=None)

plant_production_rates = pd.read_csv('Information/PlantProductionRates.csv', names=['thermal', 'nuclear', 'combustion', 'hydro', 'wind']) 

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
trend_2015 = pd.read_csv('PastYearData/NBTrend2015.csv', header=None)
trend_2015['months'] = months.copy()

trend_2016 = pd.read_csv('PastYearData/NBTrend2016.csv', header=None)
trend_2016['months'] = months.copy()

trend_2017 = pd.read_csv('PastYearData/NBTrend2017.csv', header=None)
trend_2017['months'] = months.copy()

trend_2018 = pd.read_csv('PastYearData/NBTrend2018.csv', header=None)
trend_2018['months'] = months.copy()

pass