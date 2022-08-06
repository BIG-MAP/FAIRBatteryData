"""Demonstrate use of a postgresql database
"""
import dlite


thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
datadir = thisdir.parent / 'data'
ontodir = thisdir.parent / 'ontologies'

# Add metadata to search path
dlite.storage_path.append(f'{entitydir}/BatteryCycleData.json')

# Load from postgresql db
host = 'postgres.sintef.no'
user = 'jesperf@sintef.no'
database = 'jesperf-bigmap'

dlite.Instance.from_url(f'postgresql://{host}?{user=};{database=}')
