# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 18:53:58 2022

@author: simonc
"""
from pathlib import Path
import os
import dlite

# set directory information
thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'

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

cell.save('json', f'{thisdir}/output/battery_cell_metadata.json', 'mode=w')
