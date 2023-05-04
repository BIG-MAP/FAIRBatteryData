import streamlit as st
import pandas as pd
import json
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, RDFS, SKOS

@st.cache_data
def load_ontology():
    emmo                        = 'https://emmo-repo.github.io/versions/1.0.0-beta3/emmo-inferred.ttl'
    quantities                  = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/isq_bigmap.ttl'
    units                       = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/unitsextension_bigmap.ttl'
    electrochemical_quantities  = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/electrochemicalquantities.ttl'
    electrochemistry            = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/electrochemistry.ttl'
    battery_quantities          = 'https://raw.githubusercontent.com/emmo-repo/domain-battery/master/batteryquantities.ttl'
    battery                     = 'https://raw.githubusercontent.com/emmo-repo/domain-battery/master/battery.ttl'
    materials                   = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/material_bigmap_temp.ttl'

    kg_path_mod                 = 'https://raw.githubusercontent.com/BIG-MAP/FAIRBatteryData/json-ld/app/kg-battery-mod.ttl'
    experts                     = 'https://raw.githubusercontent.com/BIG-MAP/FAIRBatteryData/json-ld/app/BatteryExperts.ttl'

    g= Graph()
    g.parse(emmo, format='ttl')
    g.parse(quantities, format='ttl')
    g.parse(units, format='ttl')
    g.parse(electrochemical_quantities, format='ttl')
    g.parse(electrochemistry, format='ttl')
    g.parse(battery_quantities, format='ttl')
    g.parse(battery, format='ttl')
    g.parse(materials, format='ttl')
    g.parse(kg_path_mod, format='ttl')
    g.parse(experts, format='ttl')
    
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

def upload_files(g):
    with st.expander("Upload Cell Profile From File (Optional)"):
        #json_dict = {}
        #g = Graph()
        uploaded_files = st.file_uploader("Upload a JSON-LD metadata profile", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            content = uploaded_file.read()
            data = json.loads(content.decode('utf-8'))
            g.parse(data=json.dumps(data), format="json-ld")

        return g
    
def get_cell_iri(g):

    cell_iri = []
    query_text = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?s
    WHERE {
    ?s rdf:type/rdfs:subClassOf* <http://emmo.info/battery#battery_68ed592a_7924_45d0_a108_94d6275d57f0> .
    }
    """
    results = g.query(query_text)
    for row in results:
        cell_iri.append(row.s)

    return str(cell_iri[0])

def get_cell_name(g, iri):
    name = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?o
    WHERE {{
    <{iri}> schema:name ?o .
    }}
    """
    results = g.query(query_text)
    for row in results:
        name.append(row.o)

    return str(name[0])

def get_creator(g, iri):
    creator = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?o
    WHERE {{
    <{iri}> schema:creator ?o .
    }}
    """
    results = g.query(query_text)
    for row in results:
        creator.append(row.o)

    return str(creator[0])

def get_productionDate(g, iri):
    productionDate = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?o
    WHERE {{
    <{iri}> schema:productionDate ?o .
    }}
    """
    results = g.query(query_text)
    for row in results:
        productionDate.append(row.o)

    return str(productionDate[0])

def get_manufacturer(g, iri):
    manufacturer = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?o
    WHERE {{
    <{iri}> schema:manufacturer ?o .
    }}
    """
    results = g.query(query_text)
    for row in results:
        manufacturer.append(row.o)

    return str(manufacturer[0])

def get_format(g, iri):
    format = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?o
    WHERE {{
    <{iri}> rdf:type ?o .
    }}
    """
    results = g.query(query_text)
    for row in results:
        format.append(row.o)

    return str(format[0])

def get_positive_active_material(g, iri):
    pe_active_material = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?o
    WHERE {{
    <{iri}> <http://emmo.info/electrochemistry#electrochemistry_8e9cf965_9f92_46e8_b678_b50410ce3616> ?pe .
    ?pe <http://emmo.info/emmo#EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec> ?coating .
    ?coating <http://emmo.info/emmo#EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec> ?o .
    ?o rdf:type* <http://emmo.info/emmo#EMMO_321ea507_e363_4676_80dc_7f7f566ce2e2> .
    }}
    """
    results = g.query(query_text)
    for row in results:
        pe_active_material.append(row.o)

    return str(pe_active_material[0])

def get_datasets(g, iri):
    datasets = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    SELECT ?ds
    WHERE {{
    ?ds dcterms:subject ?o .
    }}
    """
    #?ds dcterms:subject <{iri}> .
    results = g.query(query_text)
    for row in results:
        datasets.append(row.ds)

    return str(datasets[0])


def get_data(g, cell_iri, uri_label_dict):
    name = get_cell_name(g, cell_iri)
    creator = get_creator(g, cell_iri)
    manufacturer = get_manufacturer(g, cell_iri)
    format = uri_label_dict[get_format(g, cell_iri)].replace("Cell", "")
    datasets = get_datasets(g, cell_iri)
    #pe_material = uri_label_dict[get_positive_active_material(g, cell_iri)]

    #format = "Coin"
    capacity = "200 mAh"
    pe_material = "LFP"
    ne_material = "Graphite"

    productionDate = "2023-05-04"
    #creator = "ORCID"
    #manufacturer = "RORID"
    reference = "DOI"

    return{
        "IRI": cell_iri,
        "name": name,
        "format": format,
        "capacity": capacity,
        "pe_material": pe_material,
        "ne_material": ne_material,
        "productionDate": productionDate,
        "creator": creator,
        "manufacturer": manufacturer,
        "reference": reference,
        "datasets": datasets
    }

g, label_uri_dict, uri_label_dict = load_ontology()


json_g = upload_files(g)
# if json_g is not None:
#     for s, p, o in json_g:
#         st.write(s, p, o)

cell_iri = get_cell_iri(json_g)
dict = get_data(json_g, cell_iri, uri_label_dict)

st.metric(dict["IRI"], dict["name"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Format", dict["format"])
col2.metric("Capacity", dict["capacity"])
col3.metric("Positive Active Material", dict["pe_material"])
col4.metric("Negative Active Material", dict["ne_material"])

with st.expander("Production Details"):
    # st.text_input("Production Date", value=dict["productionDate"], disabled=True)
    # st.text_input("Creator", value=dict["creator"], disabled=True)
    # st.text_input("Manufacturer", value=dict["manufacturer"], disabled=True)
    col1, col2 = st.columns([1,3])
    with col1:
        st.write("Production Date:")
        st.write("Creator:")
        st.write("Manufacturer:")
    with col2:
        st.write(dict["productionDate"])
        st.write(dict["creator"])
        st.write(dict["manufacturer"])

with st.expander("Datasets"):
    st.write(dict["datasets"])

with st.expander("References"):
    st.text_input("Reference", value=dict["reference"], disabled=True)