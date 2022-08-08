"""Demonstrate use of large datasets.
"""
from pathlib import Path

import dlite


# Paths
thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
datadir = thisdir.parent / 'data'
ontodir = thisdir.parent / 'ontologies'

# Add metadata to search path
dlite.storage_path.append(f'{entitydir}/BatteryCycleDataExtended.json')

# Load dataset
uri = 'http://onto-ns.com/meta/0.1/BatteryCycleDataExtended'
id = 'timeseries-extended-2012-05-22-no1'  # Give the dataset a human name
data = dlite.Instance.from_location(
    driver='csv',
    #location=datadir / 'BatteryTimeSeriesData/timeseries-full.xlsx',
    location=datadir / 'BatteryTimeSeriesData/timeseries-full-csv.csv',
    options=f'infer=false;meta={uri};id={id}',
)

print('Number of rows:', data.rows)
