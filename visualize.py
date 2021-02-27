import pandas as pd
import numpy as np 
import plotly.graph_objects as go

# Get all variables as values from parse.py
from parse import *


energy_trends = [trend_2015, trend_2016, trend_2017, trend_2018]
all_energy_data = pd.concat(energy_trends).reset_index().drop(labels=["index"], axis=1)

print(all_energy_data)
# print(penalty_values)
# print(plant_production_rates)
# print(emission_tax)
# print(non_emission_tax)


# get all of the energy from one of the 




