from parse import *
from power_consumption_predict import *
from visualize import *

# Generate all models from given trend data


if __name__ == '__main__':
    # Level 1
    # Calculate power usage (and convert to GWh)
    predicted_power_usage = get_predicted_power_usage(2022).divide(1000000)
    # Display output:
    visualize_data(predicted_power_usage)
    # output results to csv:
    predicted_power_usage.to_csv(r"./L1_output.csv")

    # Level 2
    

