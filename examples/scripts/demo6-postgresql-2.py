"""Demonstrate use of a postgresql database

This script reads an instance from postgres.sintef.no.

See demo6-postgresql-1.py for connection details.
"""
from pathlib import Path

import dlite


# Database setup
host = 'postgres.sintef.no'
user = 'jesperf@sintef.no'  # Change this line to your username
database = 'jesperf-bigmap'

# Paths
thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
datadir = thisdir.parent / 'data'
ontodir = thisdir.parent / 'ontologies'

# Add metadata to search path
dlite.storage_path.append(f'{entitydir}/BatteryCycleData.json')

# Load from postgresql db
data = dlite.Instance.from_location(
    driver='postgresql',
    location=host,
    options=f'user={user};database={database}',
    id = 'timeseries-mini-2012-05-22-no1',
)

print(data)
