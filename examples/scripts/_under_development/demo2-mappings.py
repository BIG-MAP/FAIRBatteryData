"""Second part of demo2 -
This reads the results from demo2-conformToDataModel.py
"""
import os
from re import I
import time
from pathlib import Path

import numpy as np

import dlite
from dlite.triplestore import (
    en, Literal, Triplestore,
    EMMO, OWL, RDF, RDFS, SKOS, XSD,
)
from dlite.mappings import instantiate
from dlite.mappings import mapping_route

import pint

from scipy import integrate


thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
ontodir = thisdir.parent / 'ontologies'


# Add unit Ah to unit registry
ureg = pint.UnitRegistry()
ureg.define('Ah  = A * h')


# Read data from first part of demo2
#dlite.storage_path.append(entitydir)
datamodel = "cycledatamodel.json"
datamodel_path = os.path.join(outputdir, datamodel)
CycleData = dlite.Instance.from_url(f'json://{datamodel_path}')
BatteryData = dlite.Instance.from_url(
    f'json://{entitydir}/BatteryTimeSeriesData.json')


cycledata = dlite.Instance.from_location(
    'json', f'{thisdir}/output/cycledata_raw.json', 'mode=r')


ts = Triplestore("rdflib")
ts.parse(f"{ontodir}/battinfo-merged.ttl")

# BattINFO namespace
BATTINFO = ts.bind(
    'battinfo', 'https://big-map.github.io/BattINFO/ontology/BattINFO#')


# Dict mapping prefLabel to IRI
# TODO: we should add more convenient support for handling prefLabel
d = {o.value: s for s, o in ts.subject_objects(SKOS.prefLabel)}


## TODO: Move below triples to BattINFO

# Add ontological concept for time stamp
TimeStamp = BATTINFO['EMMO_d597d7b7-2d35-5d97-9cf1-622b8dfb7d24']
d['TimeStamp'] = TimeStamp
ts.add((TimeStamp, RDF.type, OWL.Class))
ts.add((TimeStamp, RDFS.subClassOf, OWL.Class))
ts.add((TimeStamp, SKOS.prefLabel, en('TimeStamp')))
ts.add((TimeStamp, d['elucidation'],
        en('The time of a data point in a time serie.')))

# Add timeFormat data property
timeFormat = BATTINFO['EMMO_eeef9cd8-9e15-54a7-93fe-a1c20c8372cb']
d['timeFormat'] = timeFormat
ts.add((timeFormat, RDF.type, OWL.DatatypeProperty))
ts.add((timeFormat, RDF.type, OWL.FunctionalProperty))
ts.add((timeFormat, RDFS.subPropertyOf, d['hasSymbolData']))
ts.add((timeFormat, RDFS.domain, TimeStamp))
ts.add((timeFormat, RDFS.range, XSD.string))
ts.add((timeFormat, SKOS.prefLabel, en('timeFormat')))
ts.add((timeFormat, d['elucidation'],
        en('A time format string according to strptime().')))

# Add TimeStamp subclass for times in seconds since start
TimeStamp_S = BATTINFO['EMMO_fb0da9cf-6b89-5072-bf5a-66e32c8cd6f6']
d['TimeStamp_S'] = TimeStamp_S
ts.add((TimeStamp_S, RDF.type, OWL.Class))
ts.add((TimeStamp_S, RDFS.subClassOf, TimeStamp))
ts.add((TimeStamp_S, SKOS.prefLabel, en('TimeStamp_S')))
ts.add((TimeStamp_S, timeFormat, Literal('%S')))
ts.add((TimeStamp_S, d['elucidation'],
        en('The time of a data point in seconds since start.')))

# Add TimeStamp subclass for HHMMSS format
TimeStamp_HHMMSS = BATTINFO['EMMO_d14fff96-4fbe-5e1c-920e-d83c926ba179']
d['TimeStamp_HHMMSS'] = TimeStamp_HHMMSS
ts.add((TimeStamp_HHMMSS, RDF.type, OWL.Class))
ts.add((TimeStamp_HHMMSS, RDFS.subClassOf, TimeStamp))
ts.add((TimeStamp_HHMMSS, SKOS.prefLabel, en('TimeStamp_HHMMSS')))
ts.add((TimeStamp_HHMMSS, timeFormat, Literal('%H:%M:%S')))
ts.add((TimeStamp_HHMMSS, d['elucidation'],
        en('The time of a data point in HHMMSS format.')))


# Add mappings
ts.add_mapsTo(d['InstantaneousCurrent'], BatteryData, 'battery_current')
ts.add_mapsTo(d['InstantaneousCurrent'], cycledata.meta, 'Current')
ts.add_mapsTo(d['CellVoltage'], BatteryData, 'battery_voltage')
ts.add_mapsTo(d['CellVoltage'], cycledata.meta, 'Voltage')
ts.add_mapsTo(d['TimeStamp_S'], BatteryData, 'test_time')
ts.add_mapsTo(d['TimeStamp_HHMMSS'], cycledata.meta, 'Test_Time')


def anytime2seconds(anytime, format):
    """Help function that converts `anytime`, which is a single time datum
    to number of seconds since EPOCH (normally January 1, 1970, 00:00:00 UTC).

    The `format` argument specifies how `anytime` is formatted.
    See the documentation of time.strptime() for format specification.

    """
    # If `anytime` is a pint.Quantity, convert it to seconds
    if hasattr(anytime, 'm_as'):
        anytime = anytime.m_as('s')

    st = time.strptime(anytime, format)

    # If anytime contains no year, it defaults to 1900. But Windows
    # cannot handle times before 1970.  As a workaround, we truncate
    # all times before 1970 before calling time.mktime() and then
    # subtract the offset.
    if st.tm_year < 1970:
        offset = 1970 - st.tm_year
        st = list(st)
        st[0] = 1970  # year is the first field in struct_time `st`
        seconds_per_year = 31556952
        return time.mktime(tuple(st)) - offset*seconds_per_year
    else:
        return time.mktime(st)


# Define conversion functions
def timeconvert(times, format):
    """Convert an array of time stamps to seconds since the start.

    The `format` argument specifies the time format in the input.
    See the documentation of time.strptime() for format specification.
    """
    seconds = [anytime2seconds(t, format) for t in times]
    starttime = seconds[0]
    return np.array([t - starttime for t in seconds])


def timeconvert_HHMMSS(times):
    """Convert timestamps in "HH:MM:SS" format to seconds from start."""
    return timeconvert(times, "%H:%M:%S")


def calculate_capacity(test_time, battery_current):
    battery_capacity = integrate.cumtrapz(
        test_time, battery_current, initial = 0)
    return battery_capacity


def calculate_energy(test_time, battery_current, battery_voltage):
    battery_energy = integrate.cumulative_trapezoid(
        battery_current * battery_voltage, test_time, initial=0)
    return battery_energy


# Add ontological description of conversion functions
ts.add_function(
    func=timeconvert_HHMMSS,
    expects=[d['TimeStamp_HHMMSS']],
    returns=[d['TimeStamp_S']],
    base_iri=BATTINFO,
)

# Calculate capacity
calculate_capacity_IRI = ts.add_function(
    func = calculate_capacity,
    expects=[d['TimeStamp_S'], d['InstantaneousCurrent']],
    returns=[d['Capacity']],
    base_iri = BATTINFO,
)

# Calculate energy
calculate_energy_IRI = ts.add_function(
    func = calculate_energy,
    expects=[d['TimeStamp_S'], d['InstantaneousCurrent'], d['CellVoltage']],
    returns=[d['BatteryEnergy']],
    base_iri = BATTINFO,
)


# Create BatteryData instance populated via ontological mappings
inst = instantiate(
    meta=BatteryData.uri,
    instances=[cycledata],
    triplestore=ts,
    allow_incomplete=True,
    quantity=ureg.Quantity,  # with our custum units
)

print()
print('inst.test_time:')
print(inst.test_time)

print()
print('inst.battery_current:')
print(inst.battery_current)

cap = calculate_capacity(inst.test_time, inst.battery_current)
print()
print('calcualted capacity')
print(cap)

ene = calculate_energy(
    inst.test_time, inst.battery_current, inst.battery_voltage)
print()
print('calcualted energy')
print(ene)

inst.save('json', f'{thisdir}/output/cycledata_instance_mapped.json', 'mode=w')