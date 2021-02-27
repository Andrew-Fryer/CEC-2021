import pandas as pd
import numpy as np
import plotly.graph_objects as go

# importing custom memory tracking decorator
from track_memory import track_memory_use, plot_memory_use

# Get all variables as values from parse.py
from parse import *

@track_memory_use(close=False, return_history=True, plot=True)
def visualize_data(pred_consumption):
    energy_trends = [trend_2015, trend_2016, trend_2017, trend_2018]
    all_energy_data = pd.concat(energy_trends).reset_index().drop(
        labels=["index"], axis=1)

    dates = [' '.join(i) for i in zip(
        all_energy_data["months"], all_energy_data["year"].map(str))]

    fig = go.Figure()
    colours = ["#F8B195",
               "#F67280",
               "#C06C84",
               "#6C5B7B",
               "#355C7D",
               "#99B898",
               "#547980"]
    newMonthLabels = [f"{month} 2022" for month in months]

    actual_energy = all_energy_data.drop(labels=["year", "months"], axis=1).divide(1000000)

    for zone, index, colour in zip(actual_energy, pred_consumption, colours):
        actual = go.Scatter(x=dates,
                            y=actual_energy[zone],
                            name=f'{zone} Actual',
                            line=dict(color=colour))
        predicted = go.Scatter(x=newMonthLabels,
                               y=pred_consumption[index],
                               name=f'{zone} Predicted',
                               line=dict(color=colour, dash='dash'),
                               mode="lines")
        fig.add_traces([actual, predicted])

    fig.update_layout(template="ggplot2",
                      title=dict(
                          text="Prediction of Power Usage Per Month By Zone",
                          font=dict(
                              size=36
                          )
                      ),
                      xaxis_title="Month and Year",
                      yaxis_title="Power Requirements (GWh)",
                      legend_title="Legend")
    fig.show()


def visualize_mem_use(memory_usage):
    fig = go.Figure()
    samples_num = len(memory_usage[1])
    fig.add_trace(go.Scatter(x=np.linspace(0,samples_num/1000,samples_num), y=memory_usage[1]))
    fig.show()