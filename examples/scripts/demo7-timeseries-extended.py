"""Demonstrate loading of a large datasets.
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

# Load the dataset
#
# Instead of generating a new metadata for this dataset, we uses the
# already defined http://onto-ns.com/meta/0.1/BatteryCycleDataExtended.
# This is achieved via the options "infer=false" and "meta=..." options
# to dlite.Instance.from_location(). One main benefit of this is that
# the metadata can be stored in a repository and reused in other settings.
# Another important benefit is that the metadata is know before loading
# the dataset, making it much easier to write a script or program that uses
# the dataset.
#
# In order to create the metadata in the first place, we asked dlite to
# generate a draft for the metadata by commenting out the options argument
# to dlite.Instance.from_location() and uncomminging the last line of this
# script.  We then manually edited the `uri` and `description` of the
# generated json file before saving it in the entities/ directory.
#
# The option "id=timeseries-extended-2012-05-22-no1" gives the dataset
# human readable name.  This makes it possible to refer to this dataset
# by this id in addition to its uuid.
uri = 'http://onto-ns.com/meta/0.1/BatteryCycleDataExtended'
id = 'timeseries-extended-2012-05-22-no1'  # Give the dataset a human name
data = dlite.Instance.from_location(
    driver='csv',
    #location=datadir / 'BatteryTimeSeriesData/timeseries-full.xlsx',
    location=datadir / 'BatteryTimeSeriesData/timeseries-full-csv.csv',
    # Comment out the below line to automatically generate the metadata
    options=f'infer=false;meta={uri};id={id}',
)

print('Number of rows:', data.rows)


# Saving the metadata
#data.meta.save('json', 'BatteryCycleDataExtended.json')
