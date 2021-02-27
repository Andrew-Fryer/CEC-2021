from parse import *
from power_consumption_predict import *
from visualize import *

# Generate all models from given trend data
models = []
models.append(generate_models(trend_2015))
models.append(generate_models(trend_2016))
models.append(generate_models(trend_2017))
models.append(generate_models(trend_2018))

#predicted_power_usage = get_predicted_power_usage(models, 2016)

# visualize_data(models)
