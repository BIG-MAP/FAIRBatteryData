"""Simple demo for reading a xslx file using oteapi-dlite.

This example uses oteapi_dlite directly skipping otelib.
"""
from pathlib import Path

import dlite
from oteapi.datacache import DataCache
from oteapi_dlite.strategies.parse_excel import DLiteExcelStrategy
#from oteapi.plugins import create_strategy


thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'

coll_raw = dlite.Collection()
coll_processed = dlite.Collection()

def readRwthData(filename):
    # Add the content of the xlsxfile to the datacache (like what the
    # download strategy would have done)
    cache_key = DataCache().add(filename.read_bytes())

    config = {
        "downloadUrl": filename.as_uri(),
        "mediaType": "application/vnd.dlite-xlsx",
        "configuration": {
            "excel_config": {
                "worksheet": "rawdata",
                "header_row": "1",
                "row_from": "2",
            },
        },
    }


    session = {"collection_id": coll_raw.uuid, "key": cache_key}

    parser = DLiteExcelStrategy(config)
    session.update(parser.initialize(session))

    # This is the interesting part
    parser = DLiteExcelStrategy(config)
    parser.get(session)

    CycleData = dlite.Instance.from_url(f'json://{entitydir}/BatteryCyclingTimeSeriesData.json')
    data = coll_raw.get("excel-data")
    inst = CycleData(dims=[len(data.Strom),1])
    inst.current = data.Strom
    inst.voltage = data.Spannung
    inst.battery_temperature = data.Temp1
    return inst

filename = (thisdir / "../data/BatteryTimeSeriesData/rwth_data" /
           "rwth_example_data.xlsx")
inst = readRwthData(filename)
casename = filename.stem
coll_processed.add(label=casename, inst=inst)

inst.save('json', f'{thisdir}/output/rwth_cycledata_instance.json', 'mode=w')
# coll_processed.save('json', f'{thisdir}/output/rwth_cycledata_collection_processed.json', 'mode=w')
