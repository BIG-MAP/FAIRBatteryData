# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:41:39 2022

@author: simonc
"""
import ontopy

onto = ontopy.get_ontology("C:\\Users\\simonc\\Documents\\GitHub\\BattINFO\\battinfo.ttl")
onto.load()

onto.Battery
onto.Battery.ancestors()
onto.Battery.is_a

B = onto.Battery
print(B.get_iri(B))