
from rdflib import Graph, SKOS, Literal, URIRef, RDF
from rdflib.parser import Parser
import warnings
import pickle

import pandas as pd



PATH_JSONLD = "../ontologies/scientific_metadata.json"



#######################################
# TYPES
#######################################

def all_types(iri_label_dict:dict, metadata_graph:Graph)->dict:
    
    json_ld_types = {}

    for _, o in metadata_graph.subject_objects(RDF.type):

        if isinstance(o, URIRef):
            uri = str(o)

            if uri in iri_label_dict:
                uri_label = iri_label_dict[uri]
                json_ld_types[uri_label] = uri

    return json_ld_types





#######################################
# LOAD ONTOLOGIES
#######################################

def load_ontologies():
    emmo =                       'https://emmo-repo.github.io/versions/1.0.0-beta3/emmo-inferred.ttl'
    quantities =                'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/isq_bigmap.ttl'
    units =                     'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/unitsextension_bigmap.ttl'
    electrochemical_quantities = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/electrochemicalquantities.ttl'
    electrochemistry =          'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/electrochemistry.ttl'
    battery_quantities =        'https://raw.githubusercontent.com/emmo-repo/domain-battery/master/batteryquantities.ttl'
    battery =                   'https://raw.githubusercontent.com/emmo-repo/domain-battery/master/battery.ttl'
    kg_path_mod =               'https://raw.githubusercontent.com/BIG-MAP/FAIRBatteryData/json-ld/app/kg-battery-mod.ttl'
    materials =                 "https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/material_bigmap_temp.ttl"
    experts =                   'https://raw.githubusercontent.com/BIG-MAP/FAIRBatteryData/json-ld/app/BatteryExperts.ttl'

    g= Graph()
    g.parse(emmo, format='ttl')
    g.parse(quantities, format='ttl')
    g.parse(units, format='ttl')
    g.parse(electrochemical_quantities, format='ttl')
    g.parse(electrochemistry, format='ttl')
    g.parse(battery_quantities, format='ttl')
    g.parse(battery, format='ttl')
    g.parse(kg_path_mod, format='ttl')
    g.parse(experts, format='ttl')
    g.parse(materials, format='ttl')

    # Create a dictionary to hold the mappings
    label_uri_dict = {}
    uri_label_dict = {}

    # Iterate through all the triples in the graph
    for subj, pred, obj in g:

    # Check if the predicate is `skos:prefLabel`
        if pred == SKOS.prefLabel and isinstance(obj, Literal):

    # Store the URI and prefLabel in the dictionary
            label_uri_dict[obj.value] = subj
            uri_label_dict[str(subj)] = obj.value

    return g, label_uri_dict, uri_label_dict
    

def load_resources():

    jsons_paths = ["../ontologies/scientific_metadata.json",
                    "../ontologies/experts.json",
                    "../ontologies/organizations.json", 
                    "../ontologies/SINTEFCell20230502-1-1.json", 
                    "../ontologies/SINTEFCell20230502-2-1.json", 
                    "../ontologies/SINTEFCell20230502-3-1.json", 
                    "../ontologies/SINTEFCell20230502-4-1.json"]

    g, label_uri_dict, uri_label_dict = load_ontologies()

    for path in jsons_paths:
        g_json = Graph().parse(path, format='json-ld')
        g = g + g_json


    return g, label_uri_dict, uri_label_dict


def pickle_resources():

    g, label_uri_dict, uri_label_dict = load_resources()

    # Pickle the RDF graph object
    with open("rdf_ontologies_kb.pickle", "wb") as f:
        pickle.dump(g, f)

    with open("label_uri_dict.pickle", "wb") as f:
        pickle.dump(label_uri_dict, f)

    with open("uri_label_dict.pickle", "wb") as f:
        pickle.dump(uri_label_dict, f)


def unpickle_resources():
    # Unpickle the RDF graph object
    with open("rdf_ontologies_kb.pickle", "rb") as f:
        g_unpickled = pickle.load(f)

    with open("label_uri_dict.pickle", "rb") as f:
        label_uri_dict = pickle.load(f)

    with open("uri_label_dict.pickle", "rb") as f:
        uri_label_dict = pickle.load(f)

    return g_unpickled, label_uri_dict, uri_label_dict


#################################
#   ABSTRACTED FUNCTIONS
################################

def get_all_ld_types():
    g, label_uri_dict, uri_label_dict = load_ontologies()
    metadata_graph = Graph().parse(PATH_JSONLD)
    types_dict = all_types(uri_label_dict, metadata_graph)
    return types_dict




#################################
#   QUERIES
################################
PREFIXES = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX emmo: <http://emmo.info/emmo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX echem: <http://emmo.info/electrochemistry#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dc: <http://purl.org/dc/elements/1.1/> 
PREFIX battery: <http://emmo.info/battery#> 
PREFIX schema:<https://schema.org/>
"""



def query_all_schemas(rdf_graph:Graph, uri_label_dict:dict, schema_type:str)->list:
   
   supported_schema_entities =  ["name", "manufacturer", "creator"]
   
   if schema_type in supported_schema_entities:

        query = PREFIXES + """
        SELECT ?variable
        WHERE {{
            ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
                        schema:{schema} ?variable.
        }}
        """.format(schema= schema_type)

        qres = rdf_graph.query(query)

        for result in qres:
            iris_str = [str(uriref) for uriref in result]
            iris_labels = [uri_label_dict[iri] if iri in uri_label_dict else iri for iri in iris_str]
        
        return [*iris_labels]
   
   else:
       warnings.warn("Schema type not available. Available schema: are {}".format(supported_schema_entities))


def query_all_materials(rdf_graph:Graph, uri_label_dict:dict)->list:

    query = PREFIXES  + """

    SELECT ?chemicalmaterial
    WHERE {
        ?instance rdf:type/rdfs:subClassOf* battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
                (echem:electrochemistry_8e9cf965_9f92_46e8_b678_b50410ce3616|echem:electrochemistry_5d299271_3f68_494f_ab96_3db9acdd3138) ?something.

        ?something (emmo:EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec)+ ?material.
        ?material rdf:type ?chemicalmaterial.

        ?chemicalmaterial rdfs:subClassOf emmo:EMMO_8a41ed1b_64f9_4be7_9b60_01fcece45075.
    }
    """

    qres = rdf_graph.query(query)

    materials = {}

    for result in qres:
        iri_str = str(result[0])
        iri_label = uri_label_dict[iri_str]
        if iri_label not in materials:
            materials[iri_label] = iri_str

    return materials





def query_cell_by_material(rdf_graph:Graph, label_uri_dict:dict, uri_label_dict:dict, material_label:str)->pd.DataFrame:

    material_iri = URIRef(label_uri_dict[material_label])
    print(material_iri)

    query_by_material = PREFIXES  + """
    SELECT ?instance ?name ?creator ?date
    WHERE {{
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
              schema:creator ?creator;
              schema:name ?name;
              schema:productionDate ?date;
              (echem:electrochemistry_8e9cf965_9f92_46e8_b678_b50410ce3616|echem:electrochemistry_5d299271_3f68_494f_ab96_3db9acdd3138) ?something.

    ?something (emmo:EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec)+ ?material.
    ?material rdf:type <%s>.

    }}
    """% material_iri    

    results_dict = {"CellID":[], "Cell name":[], "Creator":[], "Date":[], "Material":[]}

    qres = rdf_graph.query(query_by_material)
    for hit in qres:
        string_rep = [str(rdf_obj) for rdf_obj in hit]
        human_rep = [uri_label_dict[string] if string in uri_label_dict else string for string in string_rep]
        results_dict["CellID"].append(human_rep[0])
        results_dict["Cell name"].append(human_rep[1])
        results_dict["Creator"].append(human_rep[2])
        results_dict["Date"].append(human_rep[3])
        results_dict["Material"].append(material_label)
    
    return pd.DataFrame(results_dict)



def query_all_experts(rdf_graph:Graph)->dict:

    query = PREFIXES  + f"""
        SELECT ?givenName ?familyName ?id

        WHERE {{
            ?id rdf:type schema:Researcher;
                        schema:familyName ?familyName;
                        schema:givenName ?givenName.
        }}
        """


    qres = rdf_graph.query(query)

    experts = {}
    for result in qres:
        name_str = str(result[0]) + " " + str(result[1])
        iri = str(result[2])
        experts[name_str] = iri

    return experts



def query_all_organizations(rdf_graph:Graph)->dict:

    query = PREFIXES  + f"""
    SELECT ?name ?id

    WHERE {{
        ?id rdf:type schema:ResearchOrganization;
                schema:name ?name;
    }}
    """
    qres = rdf_graph.query(query)


    organizations = {}
    for result in qres:
        name_str = str(result[0])
        iri = str(result[1])
        organizations[name_str] = iri

    return organizations


def query_cell_by_expert(rdf_graph:Graph, expert_orcid:str):

    query = PREFIXES  + f"""
    SELECT ?instance ?givenName ?familyName ?email ?date
    WHERE {{
        ?instance rdf:type/rdfs:subClassOf* battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
                schema:creator <{expert_orcid}>;
                schema:productionDate ?date.

        <{expert_orcid}>  schema:familyName ?familyName;
                          schema:givenName ?givenName;
                         schema:email ?email.
            }}
    """

    qres = rdf_graph.query(query)

    results_dict = {"CellID":[], "Researcher":[], "Email":[], "Date":[]}

    for hit in qres:
        string_rep = [str(rdf_obj) for rdf_obj in hit]
        results_dict["CellID"].append(string_rep[0])
        results_dict["Researcher"].append(string_rep[1]+" " + string_rep[2])
        results_dict["Email"].append(string_rep[3])
        results_dict["Date"].append(string_rep[4])

    return pd.DataFrame(results_dict)


def query_cell_by_organization(rdf_graph:Graph, ror:str):

    query = PREFIXES  + f"""
        SELECT ?instance ?name ?date ?personID
        WHERE {{
            ?instance rdf:type/rdfs:subClassOf* battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
                schema:manufacturer <{ror}>;
                schema:creator ?personID;
                schema:productionDate ?date.
            <{ror}>  schema:name ?name;

            }}
        """
    qres = rdf_graph.query(query)
    results_dict = {"CellID":[], "Organization":[], "Date":[], "ResearcherID":[]}

    for hit in qres:
        string_rep = [str(rdf_obj) for rdf_obj in hit]
        results_dict["CellID"].append(string_rep[0])
        results_dict["Organization"].append(string_rep[1])
        results_dict["Date"].append(string_rep[2])
        results_dict["ResearcherID"].append(string_rep[3])
        
    return pd.DataFrame(results_dict)