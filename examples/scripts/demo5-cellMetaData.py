# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 23:15:14 2022

@author: simonc
"""
"""Simple demo for reading a xslx file using oteapi-dlite.

This example uses oteapi_dlite directly skipping otelib.
"""
from pathlib import Path
import os
import dlite
#from oteapi.datacache import DataCache
#from oteapi_dlite.strategies.parse_excel import DLiteExcelStrategy
#from oteapi.plugins import create_strategy


thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'

datamodel = "BatteryCellMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
BatteryCellMetadata = dlite.Instance.from_url(f'json://{datamodel_path}')

datamodel = "LithiumIonBatteryElectrodeMetadata.json"
datamodel_path = os.path.join(entitydir, datamodel)
PE = dlite.Instance.from_url(f'json://{datamodel_path}')



cell = BatteryCellMetadata(dims=[1])

#cell.uuid = 'sdfs-sdfsdf-sdfsdf-sdfs'
cell.positive_electrode = [PE]


#testname = xlsxfile.stem
#coll_processed.add(label=testname, inst=inst)

cell.save('json', f'{thisdir}/output/cell_metadata_instance.json', 'mode=w')
#coll_processed.save('json', f'{thisdir}/output/cycledata_collection_processed.json', 'mode=w')
