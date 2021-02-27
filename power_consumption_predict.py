from parse import * 
import numpy as np
import matplotlib.pyplot as plt

MAX_DEG = 10
MIN_DEG = 1

def generate_models(trend):
    models = []
    
    for i in range(7):
        cur_zone_data = np.array(trend['z{}'.format(i+1)])
        months = np.array([i for i in range(12)])
        
        best = None
        best_covar_sum = 1000000
        for j in range(MIN_DEG, MAX_DEG):
            model = np.polyfit(months, cur_zone_data, j, cov=True)
            covar_sum = 0
            for k in range(len(model[1])):
                covar_sum += model[1][k][k]
            if (covar_sum < best_covar_sum):
                best = model[0]
                best_covar_sum = covar_sum
        
        models.append(best)
    
    return models

def generate_monthly_adjustments(zone_models):
    monthly_models = []
    years = np.array([i for i in range(len(zone_models))])
    for i in range(12):
        annual_power_consuption = []
        for j in range(len(zone_models)):
            func = np.poly1d(zone_models[j])
            annual_power_consuption.append(func(i))
        model = np.polyfit(years, np.array(annual_power_consuption), 1)
        monthly_models.append(np.poly1d(model))
    
    return [lambda x : monthly_models[i](x)-np.poly1d(zone_models[0])(i) for i in range(12)]
    
        
models = []
models.append(generate_models(trend_2015))
models.append(generate_models(trend_2016))
models.append(generate_models(trend_2017))
models.append(generate_models(trend_2018))

zone_models = []
for i in range(7):
    to_add = []
    for j in range(len(models)):
        to_add.append(models[j][i])
    zone_models.append(to_add)

month_adj_models = []
for i in range(7):
    month_adj_models.append(generate_monthly_adjustments(zone_models[i]))
    
zone_power_pred = []
for i in range(7):
    zone_power_pred.append(lambda z, y, m : np.poly1d(models[0][z])(m) + month_adj_models[z](y))