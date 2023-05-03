import os
import streamlit as st


class Header:
    title = "# Battery Data Semantic Search"
    subtext = """Search for open repositories with battery data. 
                We use the Battery Interface Ontology [BattINFO](https://github.com/BIG-MAP/BattINFO) 
                to index multiple data repositories, and leverage semantic search to find datasets.
                When possible, the datasets can be downloaded, visualized and explored interactively."""

    def render(self):
        st.markdown(Header.title)
        st.markdown(Header.subtext)



class SelectResourceType:
    
    def __init__(self, concept_list:list):
        self.concept_list = concept_list

    def render(self):
        self.selection:str = st.selectbox(label="Search for:", options=self.concept_list)



class SelectFilters:

    def __init__(self, ontology_instances:list):
        self.ontology_instances = ontology_instances

    def render(self):
        col1, col2= st.columns((1, 4))
        col1.markdown("is")
        self.selection:str = col2.selectbox(label= "", options=self.ontology_instances, label_visibility="collapsed")



class SelectRange:

    def __init__(self, number_limits:tuple):
        self.number_limits = number_limits


    def render(self):

        col1, col2= st.columns((1, 4))

        inequality:str = col1.selectbox(options=["equal to", "greater than", "less than"], 
                                        label_visibility="collapsed")
        
        value:float = col2.number_input(min_value=self.number_limits[0],
                                        max_value=self.number_limits[1], 
                                        label_visibility="collapsed")
        
        self.selection:tuple = (inequality, value)
