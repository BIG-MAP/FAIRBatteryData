"""Demonstrate use of a postgresql database.

This script writes an instance to postgres.sintef.no.
See https://web.yammer.com/main/threads/eyJfdHlwZSI6IlRocmVhZCIsImlkIjoiMTE4Njc5NjY0ODY2OTE4NCJ9

Will only work for users that have been granted access to the database.

Linux users must authorize themselves with kinit before running this script:

    $ kinit jesperf@SINTEF.NO

"""
from pathlib import Path

import dlite


# Database setup
host = 'postgres.sintef.no'
user = 'simonc@sintef.no'  # Change this line to your username
database = 'jesperf-bigmap'

# Paths
thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
datadir = thisdir.parent / 'data'
ontodir = thisdir.parent / 'ontologies'

# Add metadata to search path
dlite.storage_path.append(f'{entitydir}/BatteryCycleData.json')

# Load dataset
uri = 'http://onto-ns.com/meta/0.1/BatteryCycleData'
id = 'timeseries-mini-2012-05-22-no1'  # Give the dataset a human name
data = dlite.Instance.from_location(
    driver='csv',
    location=f'{datadir}/BatteryTimeSeriesData/timeseries-mini.xlsx',
    options=f'infer=false;meta={uri};id={id}',
)

# Save to postgresql DB
data.save(f'postgresql://{host}?user={user};database={database}')
