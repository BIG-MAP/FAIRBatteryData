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

# datamodel = "BatteryElectrodeMetadata.json"
# datamodel_path = os.path.join(entitydir, datamodel)
# BatteryElectrodeMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

# datamodel = "BatteryElectrodeActiveMaterialMetadata.json"
# datamodel_path = os.path.join(entitydir, datamodel)
# BatteryElectrodeActiveMaterialMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

# datamodel = "BatteryElectrodeCurrentCollectorMetadata.json"
# datamodel_path = os.path.join(entitydir, datamodel)
# BatteryElectrodeCurrentCollectorMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

# datamodel = "BatteryElectrodeAdditiveMetadata.json"
# datamodel_path = os.path.join(entitydir, datamodel)
# BatteryElectrodeAdditiveMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

# datamodel = "BatteryElectrodeBinderMetadata.json"
# datamodel_path = os.path.join(entitydir, datamodel)
# BatteryElectrodeBinderMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

# datamodel = "BatteryElectrolyteMetadata.json"
# datamodel_path = os.path.join(entitydir, datamodel)
# BatteryElectrolyteMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

# datamodel = "BatterySeparatorMetadata.json"
# datamodel_path = os.path.join(entitydir, datamodel)
# BatterySeparatorMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

# datamodel = "BatteryCasingMetadata.json"
# datamodel_path = os.path.join(entitydir, datamodel)
# BatteryCasingMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

# create instances
cell = BatteryCellMetadata(dims=[1], id='define-some-uri')

# print result
print(cell)