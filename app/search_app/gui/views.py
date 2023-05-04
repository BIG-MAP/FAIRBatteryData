import os
import streamlit as st


class Header:
    title = "# Search Battery cells"
    subtext = """Search for manufactured cells that have been semantically annotated. 
                """

    def render(self):
        st.markdown(Header.title)
        st.markdown(Header.subtext)



class SelectCriterionAndValue:

    def __init__(self, options:dict):
        self.options = options

    def render(self):
        col1, col2= st.columns(2)
        self.criterion:str = col1.selectbox(label= "", options=self.options.keys(), label_visibility="collapsed")
        self.value:str = col2.selectbox(label= "", options=self.options[self.criterion], label_visibility="collapsed")