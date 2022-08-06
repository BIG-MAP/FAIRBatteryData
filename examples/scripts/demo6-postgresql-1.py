"""Demonstrate use of a postgresql database
"""
from pathlib import Path

import dlite


thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
datadir = thisdir.parent / 'data'
ontodir = thisdir.parent / 'ontologies'

# Add metadata to search path
dlite.storage_path.append(f'{entitydir}/BatteryCycleData.json')

# Load dataset
data = dlite.Instance.from_location(
    'csv',
    f'{datadir}/BatteryTimeSeriesData/timeseries-mini.xlsx',
    'infer=false;meta=http://onto-ns.com/meta/0.1/BatteryCycleData',
)

# Save to postgresql DB
host = 'postgres.sintef.no'
user = 'jesperf@sintef.no'
database = 'jesperf-bigmap'

data.save(f'postgresql://{host}?{user=};{database=};{password=}')
