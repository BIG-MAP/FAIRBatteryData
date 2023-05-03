import streamlit as st

import views

#########################################
#   ACCESS RESOURCES
#########################################


option_library = {"Cathode":["LiFePO4", "NMC111", "LNO"], 
                "Anode":["Graphite", "Silicon", "Si/Gr blend"], 
                "Author":["Simon Clark", "Eibar Flores", "John Wick"], 
                "Institution":["CNRS", "SINTEF", "Chalmers", "NTNU"]}

search_types = {"Battery cell":"http://emmo.info/battery#battery_68ed592a_7924_45d0_a108_94d6275d57f0",
                 "Battery Scientist":"https://schema.org/creator", 
                 "Battery dataset":"https://schema.org/Dataset"}






#########################################
#   APP HEADER
#########################################

header = views.Header()
header.render()



#########################################
#   APP SEARCH SIDEBAR
#########################################

resource_type = views.SelectResourceType(concept_list = list(search_types.keys()))
resource_type.render()



# instance = views.SelectFilters(ontology_instances=option_library[resource_type.selection])
# instance.render()
 

 #########################################
#   APP RESULTS
#########################################