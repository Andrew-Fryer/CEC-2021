from parse import *
import numpy as np
import matplotlib.pyplot as plt
import sys

# The min and max degree values for polynomial regression
MAX_DEG = 11
MIN_DEG = 1

# Number of zones to pull energy from
NUMBER_OF_ZONES = 7

# ----------------------------- Helper functions ----------------------------

'''
generate_models:
    Generates a list of 7 different polynominal regression models from given trend data
    
    trend - a dataframe obtained from parse.py
    
    output - a list for each zone containing the terms of the polynominal
'''


def generate_models(trend):
    models = []

    for i in range(NUMBER_OF_ZONES):
        # Gather zone data
        cur_zone_data = np.array(trend['z{}'.format(i+1)])
        months = np.array([i for i in range(12)])

        # Try a range of degrees, between MIN_DEG and MAX_DEG, to find optimal model
        # best = None
        # best_covar_sum = 10000000000000000000
        # for j in range(MIN_DEG, MAX_DEG):
        #     #Fit the model
        #     model = np.polyfit(months, cur_zone_data, j, cov=True)
        #     covar_sum = 0
        #     for k in range(len(model[1])):
        #         covar_sum += model[1][k][k]
        #     #If current model has lowest covariance, set it to best
        #     if (covar_sum < best_covar_sum):
        #         best = model[0]
        #         best_covar_sum = covar_sum
        best = np.polyfit(months, cur_zone_data, 10)
        models.append(best)

    return models


'''
generate_monthly_adjustments:
    Generates a list of 12 different functions to adjust the predicted power based on year
    
    zone_models - a list of the models for each year for a given zone
    
    output - a list of functions providing the adjustment needed for a given month and year
'''


def generate_monthly_adjustments(zone_models):
    monthly_models = []
    years = np.array([i for i in range(len(zone_models))])

    for i in range(12):
        # Get list of power consumption for same month, different years
        annual_power_consuption = []
        for j in range(len(zone_models)):
            func = np.poly1d(zone_models[j])
            annual_power_consuption.append(func(i))
        # Fit a linear model to adjust the year to year data for a given month
        model = np.polyfit(years, np.array(annual_power_consuption), 1)
        monthly_models.append(np.poly1d(model))

    # Return a list of functions which each take the year as an input
    return [lambda x: monthly_models[i](x)-np.poly1d(zone_models[0])(i) for i in range(12)]


# Generate all models from given trend data
models = []
models.append(generate_models(trend_2015))
models.append(generate_models(trend_2016))
models.append(generate_models(trend_2017))
models.append(generate_models(trend_2018))

# Reconfigure models generated to provide zone models
zone_models = []
for i in range(NUMBER_OF_ZONES):
    to_add = []
    for j in range(len(models)):
        to_add.append(models[j][i])
    zone_models.append(to_add)

# Generate adjustment models from zone models
month_adj_models = []
for i in range(NUMBER_OF_ZONES):
    month_adj_models.append(generate_monthly_adjustments(zone_models[i]))

# Function used to get an estimate of power consuption for a given zone, year, and month


def zone_power_pred(z, y, m): return np.poly1d(
    models[0][z])(m) + month_adj_models[z][m](y)

# --------------------------- Output Functions -------------------------------

'''
get_predicted_power_usage:
    Provides the power consumption data frame for a given year
    
    year - a year to get data for
    
    output - a dataframe in similar fashion to the given past years power consumption
'''


def get_predicted_power_usage(year):
    out = []
    for i in range(12):
        month_data = [zone_power_pred(j, year-2015, i)
                      for j in range(NUMBER_OF_ZONES)]
        out.append(month_data)
    return pd.DataFrame(out)
