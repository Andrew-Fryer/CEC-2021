from parse import * 
import numpy as np

MAX_DEG = 10
MIN_DEG = 1

def generate_models(trend):
    models = []
    
    for i in range(7):
        cur_zone_data = np.array(trend[i])
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

def generate_best_model(trends):
    months = np.array([i for i in range(12)])
    
        
models = generate_models(trend_2015)