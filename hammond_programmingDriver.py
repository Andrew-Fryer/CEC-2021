from parse import *
from power_consumption_predict import *
from visualize import *

# Generate all models from given trend data


if __name__ == '__main__':
    # Level 1
    # Display output:
    predicted_power_usage = get_predicted_power_usage(2022)
    visualize_data(predicted_power_usage)
    # output results to csv:
