# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 12:41:14 2022

@author: simonc
"""
from pathlib import Path
import os
import dlite

thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
ontodir = thisdir.parent / 'ontologies'

collection = dlite.Collection.from_location('json', f'{thisdir}/output/cell_collection.json', 'mode=r', id='5524e037-58f1-5e8c-bc68-7ce67f8d117a')

cell = collection.get('cell')
pe = collection.get('positive_electrode')

# assign properties to the instances. In this demo, we use the properties stated by Chen et al in 10.1149/1945-7111/ab9050
cell.name               = "INR21700 M50"
cell.manufacturer       = "LG Chem"


pe.coating_width        = [6.5e-2, 6.5e-2]
# pe.coating_length       = [79e-2, 79e-2]
# pe.coating_thickness    = [75.6e-6, 75.6e-6]
# pe.coating_porosity     = [0.335, 0.335]
# pe.coating_tortuosity   = [4.8, 4.8]
# pe.coating_bruggeman_coefficient = [2.43, 2.43]

# pe_am.conventional_name = 'NMC811'
# pe_am.crystal_density   = 4950
# pe_am.molecular_weight  = 94.87

# pe_cc.thickness         = 16e-6

# ne.coating_width        = [6.5e-2, 6.5e-2]
# ne.coating_length       = [77.5e-2, 83.5e-2]
# ne.coating_thickness    = [85.2e-6, 85.2e-6]
# ne.coating_porosity     = [0.25, 0.25]
# ne.coating_tortuosity   = [14.25, 13.93]
# ne.coating_bruggeman_coefficient = [2.92, 2.90]

# ne_am.conventional_name = 'Graphite-SiOx'
# ne_am.crystal_density   = 2260

# ne_cc.thickness         = 12e-6

# sep.porosity            = 0.47
# sep.tortuosity          = 3.27
# sep.thickness           = 12e-6
# sep.coated              = 'true'
