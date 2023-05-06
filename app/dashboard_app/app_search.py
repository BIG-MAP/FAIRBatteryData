import streamlit as st

import views
import utils
import pandas as pd

def search_app():



    #########################################
    #   ACCESS RESOURCES
    #########################################

    @st.cache_data
    def initialize():
        rdf_full_graph, label_uri_dict, uri_label_dict = utils.load_resources()

        option_library = {"cell name":utils.query_all_schemas(rdf_full_graph, uri_label_dict, schema_type = "name"),
                        "manufacturer":utils.query_all_organizations(rdf_full_graph),
                        "creator":utils.query_all_experts(rdf_full_graph),
                        "material":utils.query_all_materials(rdf_full_graph, uri_label_dict)}

        return option_library, rdf_full_graph, label_uri_dict, uri_label_dict


    option_library, rdf_full_graph, label_uri_dict, uri_label_dict = initialize()


    #########################################
    #   APP HEADER 
    #########################################

    header = views.Header()
    header.render()

    

    #########################################
    #   APP SEARCH CRITERIA
    #########################################

    search_criterion = views.SelectCriterionAndValue(options = option_library)
    search_criterion.render()

    search_requested = st.button("Search")


    #########################################
    #   APP SEARCH 
    #########################################
    results_df = pd.DataFrame()

    if search_requested:
        if search_criterion.criterion == "material":
            results_df = utils.query_cell_by_material(rdf_full_graph, 
                                        label_uri_dict, 
                                        uri_label_dict, 
                                        material_label=search_criterion.value)

            st.dataframe(results_df, 700, 300)

        if search_criterion.criterion == "manufacturer":

            ror_id = option_library[search_criterion.criterion][search_criterion.value]
            results_df = utils.query_cell_by_organization(rdf_full_graph, 
                                        ror=ror_id)

            st.dataframe(results_df, 700, 300)
            

        if search_criterion.criterion == "creator":

            orcid_id = option_library[search_criterion.criterion][search_criterion.value]
            results_df = utils.query_cell_by_expert(rdf_full_graph, 
                                        expert_orcid=orcid_id)

            st.dataframe(results_df, 700, 300)

    return (results_df["CellID"].to_list(), rdf_full_graph)

if __name__ == '__main__':
    results = search_app()