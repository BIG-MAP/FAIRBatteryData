# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 12:48:27 2022

@author: simonc
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

coll = dlite.Collection.from_location('json', f'{thisdir}/output/cell_collection.json', 'mode=r', id='5524e037-58f1-5e8c-bc68-7ce67f8d117a')

# cell = dlite.Instance.from_location(
#     'json', f'{thisdir}/output/battery_cell_metadata.json', 'mode=r')

# ts = Triplestore("rdflib")
# ts.parse(f"{ontodir}/battinfo-merged.ttl")

# # BattINFO namespace
# BATTINFO = ts.bind(
#     'battinfo', 'https://big-map.github.io/BattINFO/ontology/BattINFO#')

# # Dict mapping prefLabel to IRI
# # TODO: we should add more convenient support for handling prefLabel
# d = {o.value: s for s, o in ts.subject_objects(SKOS.prefLabel)}

# ts.add_mapsTo(d['Electrode'], coll, 'positive_electrode')
# ts.add_mapsTo(d['Electrode'], coll, 'negative_electrode')
# ts.add_mapsTo(d['Electrolyte'], coll, 'electrolyte')
# ts.add_mapsTo(d['Separator'], coll, 'separator')
# ts.add_mapsTo(d['BatteryCellContainer'], coll, 'casing')