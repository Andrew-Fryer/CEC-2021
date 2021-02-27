from parse import *
from power_consumption_predict import *
from visualize import *

# Generate all models from given trend data
def initialize_models(trend_2015, trend_2016, trend_2017, trend_2018):
    return [generate_models(trend_2015), 
            generate_models(trend_2016),
            generate_models(trend_2017),
            generate_models(trend_2018)]

if __name__ == '__main__':
    # Level 1
    # Display output:
    models = initialize_models(trend_2015, trend_2016, trend_2017, trend_2018)
    visualize_data(initialize_models(trend_2015, trend_2016, trend_2017, trend_2018))
    # output results to csv: 



    #predicted_power_usage = get_predicted_power_usage(models, 2016)
