# New Brunswick's Renewable Energy

New Brunswick contains many different energy sources, both renewable and non-renewable. The goal of this projects was to predict the future energy requirements
of the province based on past data, and use these predictions to maximize the renewable energy use while minimizng the power generation costs.

## Getting Started

Clone the repository with "git clone https://github.com/CEC2021Programming-ProgrammationCCI2021/hammond-hammond.git"

### (Optional) Setup Virtual Environment

`python3 -m venv venv && source venv/bin/activate`

### Installing

`pip install -r requirements.txt`

### Running

`python3 hammond_programmingDriver.py`

### Presentation

Please see `hammond_programming.pdf`

## Structure

### hammond_programmingDriver.py

Runs main project & generates output .csv files

### parse.py

Loads in data from excel files

### power_consumption_predict.py

Predicts the future energy consumption of each New Brunswick zone per month

### visualize.py

Creates the visualization of the past and predicted data

### greedy_algorithm.py (deprecated)

Simple greedy algorithm implementation for cost analysis (this approach is no longer used)

### clean_energy_types.py

Shows which energies are emissive and non-emissive

### zone_scoring.py

### algorithm.py

Contains the function which runs the optimizing algorithm on a year of energy data for New Brunswick

### zone-scoring.py (deprecated)

Initial file with thought process notes for algorithm

## Built With

python -> pandas, numpy, plotly

## Authors

Andrew Fryer
Kyle Singer
Joe Grosso
Andrew Farley

## Acknowledgments

CEC 2021 for the project idea and input data
