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




dates = [' '.join(i) for i in zip(all_energy_data["months"],all_energy_data["year"].map(str))]

fig = go.Figure()

for zone in all_energy_data.drop(labels=["year", "months"], axis=1):
    print(zone)
    fig.add_traces([go.Scatter(x=dates, y=all_energy_data[zone], name=zone)])



fig.update_layout(template="ggplot2")
fig.show()
