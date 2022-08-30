# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 18:53:58 2022

@author: simonc
"""
from pathlib import Path
import os
import dlite
from dlite.triplestore import (
    en, Literal, Triplestore,
    EMMO, OWL, RDF, RDFS, SKOS, XSD,
)
from dlite.mappings import instantiate
from dlite.mappings import mapping_route

import pint

# set directory information
thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
ontodir = thisdir.parent / 'ontologies'
datadir = thisdir.parent / 'data'

# define metadata models
datamodel = "BatteryCellMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryCellMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatteryElectrodeMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryElectrodeMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatteryElectrodeActiveMaterialMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryElectrodeActiveMaterialMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatteryElectrodeCurrentCollectorMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryElectrodeCurrentCollectorMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatteryElectrodeAdditiveMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryElectrodeAdditiveMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatteryElectrodeBinderMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryElectrodeBinderMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatteryElectrolyteMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryElectrolyteMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatterySeparatorMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatterySeparatorMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatteryCasingMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryCasingMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

collection = dlite.Collection()

# create instances
cell = BatteryCellMetadata(dims=[1], id='sdfs-sdfsdf-sdfsdf-sdfs')

pe      = BatteryElectrodeMetadata(dims=[2])
pe_am   = BatteryElectrodeActiveMaterialMetadata()
pe_cc   = BatteryElectrodeCurrentCollectorMetadata()
pe_bnd  = BatteryElectrodeBinderMetadata()
pe_add  = BatteryElectrodeAdditiveMetadata()

ne      = BatteryElectrodeMetadata(dims=[2])
ne_am   = BatteryElectrodeActiveMaterialMetadata()
ne_cc   = BatteryElectrodeCurrentCollectorMetadata()
ne_bnd  = BatteryElectrodeBinderMetadata()
ne_add  = BatteryElectrodeAdditiveMetadata()

elyte   = BatteryElectrolyteMetadata(dims=[1,1])
sep     = BatterySeparatorMetadata(dims=[1])
case    = BatteryCasingMetadata()

# create dlite collection to group instances
collection.add(label='cell', inst=cell)
collection.add(label='positive_electrode', inst=pe)
collection.add(label='positive_electrode_active_material', inst=pe_am)
collection.add(label='positive_electrode_current_collector', inst=pe_cc)
collection.add(label='positive_electrode_binder', inst=pe_bnd)
collection.add(label='positive_electrode_additive', inst=pe_add)

collection.add(label='negative_electrode', inst=ne)
collection.add(label='negative_electrode_active_material', inst=ne_am)
collection.add(label='negative_electrode_current_collector', inst=ne_cc)
collection.add(label='negative_electrode_binder', inst=ne_bnd)
collection.add(label='negative_electrode_additive', inst=ne_add)

collection.add(label='electrolyte', inst=elyte)
collection.add(label='separator', inst=sep)
collection.add(label='casing', inst=case)

# assign instances to the cell
cell.positive_electrode = [pe]
cell.positive_electrode[0].active_material = pe_am
cell.positive_electrode[0].current_collector = [pe_cc]
cell.positive_electrode[0].binder = pe_bnd
cell.positive_electrode[0].additive = pe_add

cell.negative_electrode = [ne]
cell.negative_electrode[0].active_material = ne_am
cell.negative_electrode[0].current_collector = [ne_cc]
cell.negative_electrode[0].binder = ne_bnd
cell.negative_electrode[0].additive = ne_add

cell.electrolyte = [elyte]
cell.separator = [sep]

cell.casing = [case]

# print result
print(cell)

#cell.save('json', f'{thisdir}/output/battery_cell_metadata.json', 'mode=w')
#collection.save('json', f'{thisdir}/output/cell_collection.json', 'mode=w')

ts = Triplestore("rdflib")
ts.parse(f"{ontodir}/battinfo-merged.ttl")

# BattINFO namespace
BATTINFO = ts.bind(
    'battinfo', 'https://big-map.github.io/BattINFO/ontology/BattINFO#')

# Dict mapping prefLabel to IRI
d = {o.value: s for s, o in ts.subject_objects(SKOS.prefLabel)}

# map cell components
ts.add_mapsTo(d['Electrode'], cell, 'positive_electrode')
ts.add_mapsTo(d['Electrode'], cell, 'negative_electrode')
ts.add_mapsTo(d['Electrolyte'], cell, 'electrolyte')
ts.add_mapsTo(d['Separator'], cell, 'separator')
ts.add_mapsTo(d['BatteryCellContainer'], cell, 'casing')

# map positive electrode properties
ts.add_mapsTo(d['Porosity'], pe, 'porosity')
ts.add_mapsTo(d['Tortuosity'], pe, 'tortuosity')

# assign properties to the instances. In this demo, we use the properties stated by Chen et al in 10.1149/1945-7111/ab9050
cell.name               = "INR21700 M50"
cell.manufacturer       = "LG Chem"

pe.coating_width        = [6.5e-2, 6.5e-2]
pe.coating_length       = [79e-2, 79e-2]
pe.coating_thickness    = [75.6e-6, 75.6e-6]
pe.coating_porosity     = [0.335, 0.335]
pe.coating_tortuosity   = [4.8, 4.8]
pe.coating_bruggeman_coefficient = [2.43, 2.43]

pe_am.conventional_name = 'NMC811'
pe_am.crystal_density   = 4950
pe_am.molecular_weight  = 94.87

pe_cc.thickness         = 16e-6

ne.coating_width        = [6.5e-2, 6.5e-2]
ne.coating_length       = [77.5e-2, 83.5e-2]
ne.coating_thickness    = [85.2e-6, 85.2e-6]
ne.coating_porosity     = [0.25, 0.25]
ne.coating_tortuosity   = [14.25, 13.93]
ne.coating_bruggeman_coefficient = [2.92, 2.90]

ne_am.conventional_name = 'Graphite-SiOx'
ne_am.crystal_density   = 2260

ne_cc.thickness         = 12e-6

sep.porosity            = 0.47
sep.tortuosity          = 3.27
sep.thickness           = 12e-6
sep.coated              = 'true'

# query the triplestore
query_text = """
PREFIX map: <http://emmo.info/domain-mappings#>

SELECT *
WHERE {
   ?subject map:mapsTo ?object .
}
LIMIT 200"""

query_result = ts.query(query_text)

for row in query_result:
    print(f"{row.subject} map:mapsTo {row.object}")



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

# save the collection
collection.save('json', f'{thisdir}/output/cell_collection.json', 'mode=w')
data.save('json', f'{thisdir}/output/data_extended.json', 'mode=w')
