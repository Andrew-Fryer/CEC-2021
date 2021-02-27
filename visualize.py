import pandas as pd
import numpy as np
import plotly.graph_objects as go

import power_consumption_predict

# Get all variables as values from parse.py
from parse import *


def visualize_data(models):
    energy_trends = [trend_2015, trend_2016, trend_2017, trend_2018]
    all_energy_data = pd.concat(energy_trends).reset_index().drop(
        labels=["index"], axis=1)

    dates = [' '.join(i) for i in zip(
        all_energy_data["months"], all_energy_data["year"].map(str))]

    fig = go.Figure()
    predConsumption = power_consumption_predict.get_predicted_power_usage(models,
                                                                          2022)
    colours = ["#F8B195",
               "#F67280",
               "#C06C84",
               "#6C5B7B",
               "#355C7D",
               "#99B898",
               "#547980"]
    newMonthLabels = [f"{month} 2019" for month in months]

    actual_energy = all_energy_data.drop(labels=["year", "months"], axis=1)

    for zone, index, colour in zip(actual_energy, predConsumption, colours):
        actual = go.Scatter(x=dates,
                            y=all_energy_data[zone],
                            name=f'{zone} Actual',
                            line=dict(color=colour))
        predicted = go.Scatter(x=newMonthLabels,
                               y=predConsumption[index],
                               name=f'{zone} Predicted',
                               line=dict(color=colour, dash='dash'),
                               mode="lines")
        fig.add_traces([actual, predicted])

    fig.update_layout(template="ggplot2",
                      title="Prediction of Power Usage Per Month By Zone",
                      xaxis_title="Month and Year",
                      yaxis_title="Power Requirements (GWh)",
                      legend_title="Legend Title")
    fig.show()
