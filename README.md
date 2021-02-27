# New Brunswick's Renewable Energy

Solves the Canadian Engineering Competition programming challenge for 2021.

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

### greedy_algorithm.py

### clean_energy_types.py

Shows which energies are emissive and non-emissive

### zone_scoring.py

## Built With

python -> pandas, numpy, plotly

## Authors

Andrew Fryer
Kyle Singer
Joe Grosso
Andrew Farley

## Acknowledgments

CEC 2021 for the project idea and input data
