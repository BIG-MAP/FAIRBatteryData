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
from scipy import integrate

# set directory information
thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
ontodir = thisdir.parent / 'ontologies'
datadir = thisdir.parent / 'data'

# Define metadata models

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

datamodel = "MolecularEntityMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
MolecularEntityMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "LiquidSolventMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
LiquidSolventMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatterySeparatorMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatterySeparatorMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "BatteryCasingMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryCasingMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

collection = dlite.Collection()

# create instances
cell = BatteryCellMetadata(dims=[1], id='Chen2020Example')

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
salt    = MolecularEntityMetadata()
solvent = LiquidSolventMetadata(dims=[2])
solvent_component_1 = MolecularEntityMetadata()
solvent_component_2 = MolecularEntityMetadata()

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

collection.add(label = 'electrolyte', inst=elyte)
collection.add(label = 'salt', inst=salt)
collection.add(label = 'solvent', inst=solvent)
collection.add(label = 'solvent_component_1', inst=solvent_component_1)
collection.add(label = 'solvent_component_2', inst=solvent_component_2)
collection.add(label = 'separator', inst=sep)
collection.add(label = 'casing', inst=case)

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
cell.electrolyte[0].salt = [salt]
cell.electrolyte[0].solvent_material = [solvent]
cell.electrolyte[0].solvent_material[0].molecular_entity[0]=[solvent_component_1]
cell.electrolyte[0].solvent_material[0].molecular_entity[1]=[solvent_component_2]

cell.separator = [sep]
cell.casing = [case]

# print result
print(cell)

#cell.save('json', f'{thisdir}/output/battery_cell_metadata.json', 'mode=w')
#collection.save('json', f'{thisdir}/output/cell_collection.json', 'mode=w')

# assign properties to the instances. In this demo, we use the properties stated by Chen et al in 10.1149/1945-7111/ab9050
cell.name               = "INR21700 M50"
cell.manufacturer       = "LG Chem"

pe.coating_width        = [6.5e-2, 6.5e-2]
pe.coating_length       = [79e-2, 79e-2]
pe.coating_thickness    = [75.6e-6, 75.6e-6]
pe.coating_porosity     = [0.335, 0.335]
pe.coating_tortuosity   = [4.8, 4.8]
pe.coating_bruggeman_coefficient = [2.43, 2.43]
pe.loading              = 24.69

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
ne.loading              = 14.85

ne_am.conventional_name = 'Graphite-SiOx'
ne_am.crystal_density   = 2260

ne_cc.thickness         = 12e-6

salt.conventional_name  = 'Lithium Hexafluorophosphate'
salt.linear_formula     = 'LiPF6'
salt.smiles             = '[Li+].F[P-](F)(F)(F)(F)F'
salt.molar_mass         = 151.905

solvent_component_1.conventional_name   = 'Ethylene Carbonate'
solvent_component_1.linear_formula      = 'C3H4O3'
solvent_component_1.smiles              = 'C1COC(=O)O1'
solvent_component_1.molar_mass          = 88.062 

solvent_component_2.conventional_name   = "Ethyl Methyl Carbonate"
solvent_component_2.linear_formula      = 'C4H8O3'
solvent_component_2.smiles              = 'CCOC(=O)OC'
solvent_component_2.molar_mass          = 104.10

solvent.molecular_entity_volume_fraction = [0.3, 0.7]

sep.porosity            = 0.47
sep.tortuosity          = 3.27
sep.thickness           = 12e-6
sep.coated              = 'true'

# Add metadata to search path
dlite.storage_path.append(f'{entitydir}/BatteryTimeSeriesData.json')

# Load the dataset
uri = 'http://onto-ns.com/meta/0.1/BatteryTimeSeriesData'
id = 'simualted-discharge-battmo'  # Give the dataset a human name
raw_data = dlite.Instance.from_location(
    driver='csv',
    #location=datadir / 'BatteryTimeSeriesData/timeseries-full.xlsx',
    location=datadir / 'BatteryTimeSeriesData/Chen2020_simulated_discharge.csv',
    # Comment out the below line to automatically generate the metadata
    # options=f'infer=false;meta={uri};id={id}',
)

print('Number of rows:', raw_data.rows)

datamodel = "BatteryTimeSeriesData.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryTimeSeriesData = dlite.Instance.from_url(f'json://{datamodel_path}')

processed_data = BatteryTimeSeriesData(dims=[raw_data.rows])
processed_data.test_time = raw_data.time
processed_data.battery_voltage = raw_data.voltage
processed_data.battery_current = raw_data.current
processed_data.battery_temperature = raw_data.cell_temperature
processed_data.environment_temperature = raw_data.environment_temperature


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
ts.add_mapsTo(d['Width'], pe, 'coating_width')
ts.add_mapsTo(d['Height'], pe, 'coating_length')
ts.add_mapsTo(d['Thickness'], pe, 'coating_thickness')
ts.add_mapsTo(d['MolarMass'], pe_am, 'molecular_weight')
ts.add_mapsTo(d['Thickness'], pe_cc, 'thickness')

# map negative electrode properties
ts.add_mapsTo(d['Porosity'], ne, 'porosity')
ts.add_mapsTo(d['Tortuosity'], ne, 'tortuosity')
ts.add_mapsTo(d['Width'], ne, 'coating_width')
ts.add_mapsTo(d['Height'], ne, 'coating_length')
ts.add_mapsTo(d['Thickness'], ne, 'coating_thickness')
ts.add_mapsTo(d['MolarMass'], ne_am, 'molecular_weight')
ts.add_mapsTo(d['Thickness'], ne_cc, 'thickness')

# map raw data properties
ts.add_mapsTo(d['CellVoltage'], raw_data, 'voltage')
ts.add_mapsTo(d['InstantaneousCurrent'], raw_data, 'current')

# map processed data properties
ts.add_mapsTo(d['CellVoltage'], processed_data, 'battery_voltage')
ts.add_mapsTo(d['InstantaneousCurrent'], processed_data, 'battery_current')

# query the triplestore
query_text = """
PREFIX map: <http://emmo.info/domain-mappings#>
PREFIX emmo: <http://emmo.info/emmo#>

SELECT *
WHERE {
   ?subject map:mapsTo emmo:EMMO_7f8db4c8_4dc5_4e39_bfb0_0a123679d831 .
}
"""

query_result = ts.query(query_text)

for row in query_result:
    print(f"{row.subject}")


# query the triplestore
query_text = """
PREFIX map: <http://emmo.info/domain-mappings#>
PREFIX emmo: <http://emmo.info/emmo#>
PREFIX electrochemistry: <https://big-map.github.io/BattINFO/ontology/electrochemistry#>

SELECT *
WHERE {
   ?subject map:mapsTo electrochemistry:EMMO_4ebe2ef1_eea8_4b10_822d_7a68215bd24d .
}
"""

query_result2 = ts.query(query_text)

for row in query_result2:
    print(f"{row.subject}")


# save the collection
collection.save('json', f'{thisdir}/output/cell_collection.json', 'mode=w')
raw_data.save('json', f'{thisdir}/output/data_extended.json', 'mode=w')
