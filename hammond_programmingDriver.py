from parse import *
from power_consumption_predict import *
from visualize import *
from algorithm import *

if __name__ == '__main__':
    import os

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    # Level 1
    # Calculate power usage predictions (and convert to GWh)
    predicted_power_usage, mem_history_1 = get_predicted_power_usage(2022)
    predicted_power_usage = predicted_power_usage.divide(1000000)

    # Display output of power usage (past & future):
    mem_history_2 = visualize_data(predicted_power_usage)

    # Output results of predtictions to csv:
    predicted_power_usage.columns = [
        'Zone 1 (GWh)', 'Zone 2 (GWh)', 'Zone 3 (GWh)', 'Zone 4 (GWh)', 'Zone 5 (GWh)', 'Zone 6 (GWh)', 'Zone 7 (GWh)']
    predicted_power_usage.index = months
    predicted_power_usage.to_csv(r"./L1_output.csv")

    # Level 2
    # Optimize the Costs
    costs_output = algorithm(2022)
    costs_output.columns = ['Provincial Cost ($)', 'Total Power Consumed (GWh)', 'Renewable Power Used (%)']
    costs_output.index = months
    costs_output.to_csv(r"./L2_output.csv")
