import streamlit as st
import pandas as pd
import json
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, RDFS, SKOS
import requests
import plotly.express as px
import urllib.request

from app_search import search_app


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
    experts                     = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/experts.json'
    organizations               = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/organizations.json'

    cell1 = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/SINTEF%20Cell%2020230502-1-1.json',
    cell2 = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/SINTEF%20Cell%2020230502-2-1.json'
    cell3 = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/SINTEF%20Cell%2020230502-3-1.json'
    cell4 = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/SINTEF%20Cell%2020230502-4-1.json'

    data1 = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/SINTEF%2020230502-1-1%20Discharge.json'
    data2 = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/SINTEF%2020230502-2-1%20Discharge.json'
    data3 = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/SINTEF%2020230502-3-1%20Discharge.json'
    data4 = 'https://raw.githubusercontent.com/BIG-MAP/Batt-O-Matic/main/data/SINTEF%2020230502-4-1%20Discharge.json'

    g= Graph()
    g.parse(emmo, format='ttl')
    g.parse(quantities, format='ttl')
    g.parse(units, format='ttl')
    g.parse(electrochemical_quantities, format='ttl')
    g.parse(electrochemistry, format='ttl')
    g.parse(battery_quantities, format='ttl')
    g.parse(battery, format='ttl')
    g.parse(materials, format='ttl')
    #g.parse(kg_path_mod, format='ttl')
    g.parse(experts, format='json-ld')
    g.parse(organizations, format='json-ld')

    # response = requests.get(cell1)
    # data = json.loads(response.text)
    # url = cell1
    # response = urllib.request.urlopen(url)

    # data = json.loads(response.read().decode())

    # g.parse(data=json.dumps(data), format="json-ld")


    # g.parse(cell1, format='json-ld')
    # g.parse(cell2, format='json-ld')
    # g.parse(cell3, format='json-ld')
    # g.parse(cell4, format='json-ld')
    # g.parse(data1, format='json-ld')
    # g.parse(data2, format='json-ld')
    # g.parse(data3, format='json-ld')
    # g.parse(data4, format='json-ld')
    
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

def get_cell_capacity(g, iri):
    capacity = []
    unit = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?data ?unit
    WHERE {{
    <{iri}> <http://emmo.info/emmo#EMMO_0aa934ee_1ad4_4345_8a7f_bc73ec67c7e5> ?prop .
    ?prop rdf:type <http://emmo.info/electrochemistry#electrochemistry_791c1915_a791_4450_acd8_7f94764743b5> .
    ?prop <http://emmo.info/emmo#EMMO_8ef3cd6d_ae58_4a8d_9fc0_ad8f49015cd0> ?qv .
    ?qv <http://emmo.info/emmo#EMMO_faf79f53_749d_40b2_807c_d34244c192f4> ?data .
    ?prop <http://emmo.info/emmo#EMMO_67fc0a36_8dcb_4ffa_9a43_31074efa3296> ?unit .
    }}
    """
    results = g.query(query_text)
    for row in results:
        capacity.append(row.data)
        unit.append(row.unit)

    return (capacity[0], unit[0])

def get_positive_active_material(g, iri):
    pe_active_material = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?type
    WHERE {{
    <{iri}> <http://emmo.info/electrochemistry#electrochemistry_8e9cf965_9f92_46e8_b678_b50410ce3616> ?pe .
    ?pe <http://emmo.info/emmo#EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec> ?coating .
    ?coating <http://emmo.info/emmo#EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec> ?con .
    ?con rdf:type <http://emmo.info/electrochemistry#electrochemistry_79d1b273-58cd-4be6-a250-434817f7c261> .
    ?con rdf:type ?type
    }}
    """
    results = g.query(query_text)
    for row in results:
        if str(row.type) != "http://emmo.info/electrochemistry#electrochemistry_79d1b273-58cd-4be6-a250-434817f7c261":
            pe_active_material.append(row.type)

    return str(pe_active_material[0])

def get_negative_active_material(g, iri):
    ne_active_material = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    SELECT ?type
    WHERE {{
    <{iri}> <http://emmo.info/electrochemistry#electrochemistry_5d299271_3f68_494f_ab96_3db9acdd3138> ?ne .
    ?ne <http://emmo.info/emmo#EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec> ?coating .
    ?coating <http://emmo.info/emmo#EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec> ?con .
    ?con rdf:type <http://emmo.info/electrochemistry#electrochemistry_79d1b273-58cd-4be6-a250-434817f7c261> .
    ?con rdf:type ?type
    }}
    """
    results = g.query(query_text)
    for row in results:
        if str(row.type) != "http://emmo.info/electrochemistry#electrochemistry_79d1b273-58cd-4be6-a250-434817f7c261":
            ne_active_material.append(row.type)

    return str(ne_active_material[0])

def get_datasets(g, iri):
    datasets = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    SELECT ?ds
    WHERE {{
    ?ds dcterms:subject <{iri}> .
    }}
    """
    #?ds dcterms:subject <{iri}> .
    results = g.query(query_text)
    for row in results:
        datasets.append(row.ds)

    return str(datasets[0])

def get_dataset_url(g, iri):
    accessURL = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    SELECT ?o
    WHERE {{
    <{iri}> dcat:accessURL ?o .
    }}
    """
    #?ds dcterms:subject <{iri}> .
    results = g.query(query_text)
    for row in results:
        accessURL.append(row.o)

    return str(accessURL[0])

def get_time_column(g, iri):
    order = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX echem: <http://emmo.info/electrochemistry#>
    SELECT ?order
    WHERE {{
    <{iri}> dcat:structure ?struct .
    ?struct dcat:component ?comp .
    ?comp qb:dimension echem:electrochemistry_27b3799c_250c_4332_8b71_7992c4a7bb05 .
    ?comp qb:order ?order
    }}
    """
    #?ds dcterms:subject <{iri}> .
    results = g.query(query_text)
    for row in results:
        order.append(row.order.value)

    return order[0]

def get_voltage_column(g, iri):
    order = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX echem: <http://emmo.info/electrochemistry#>
    SELECT ?order
    WHERE {{
    <{iri}> dcat:structure ?struct .
    ?struct dcat:component ?comp .
    ?comp qb:dimension <http://emmo.info/electrochemistry#electrochemistry_4ebe2ef1_eea8_4b10_822d_7a68215bd24d> .
    ?comp qb:order ?order
    }}
    """
    #?ds dcterms:subject <{iri}> .
    results = g.query(query_text)
    for row in results:
        order.append(row.order.value)

    return order[0]

def get_current_column(g, iri):
    order = []
    query_text = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <https://schema.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX echem: <http://emmo.info/electrochemistry#>
    SELECT ?order
    WHERE {{
    <{iri}> dcat:structure ?struct .
    ?struct dcat:component ?comp .
    ?comp qb:dimension <http://emmo.info/electrochemistry#electrochemistry_637ee9c4_4b3f_4d3a_975b_c0572dfe53ce> .
    ?comp qb:order ?order
    }}
    """
    #?ds dcterms:subject <{iri}> .
    results = g.query(query_text)
    for row in results:
        order.append(row.order.value)

    return order[0]

def download_dataset(url):
    # Load the CSV data into a Pandas DataFrame
    df = pd.read_csv(url)

    return df

def plot_time_voltage(g, iri, df):
    # get the order of the time and voltage from the metadata
    time_order = get_time_column(g, iri) -1
    voltage_order = get_voltage_column(g, iri) -1
    current_order = get_current_column(g, iri) -1
    # Create a line chart using Plotly
    fig = fig = px.line(df, x=df.columns[time_order], y=df.columns[voltage_order])
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    st.write(time_order, voltage_order, current_order)


def get_data(g, cell_iri, label_dict):
    name = get_cell_name(g, cell_iri)
    creator = get_creator(g, cell_iri)
    manufacturer = get_manufacturer(g, cell_iri)
    format = label_dict[get_format(g, cell_iri)].replace("Cell", "")
    datasets = get_datasets(g, cell_iri)
    accessURL = get_dataset_url(g, datasets)
    pe_material = label_dict[label_dict[get_positive_active_material(g, cell_iri)]]
    ne_material = label_dict[label_dict[get_negative_active_material(g, cell_iri)]]
    (cap_value, unit) = get_cell_capacity(g, cell_iri)

    capacity = str(cap_value) + " " + label_dict[label_dict[str(unit)]]

    #format = "Coin"
    #capacity = "200 mAh"
    #pe_material = "LFP"
    #ne_material = "Graphite"

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
        "datasets": datasets, 
        "accessURL": accessURL
    }

def search_function():
    st.write("A search bar")


g, label_uri_dict, uri_label_dict = load_ontology()

unit_prefLabel = {"kg": "Kilogram", "g": "Gram", 
             "m": "Metre", "cm": "Centimetre", "mm": "Millimetre", "micron": "Micrometre", 
             "m3": "CubicMetre", "cm3": "CubicCentimetre", "mm3": "CubicMillimetre","L": "Litre", "mL": "Millilitre", "microL": "Microlitre",
             "m2": "SquareMetre", "cm2": "SquareCentimetre", "mm2": "SquareMillimetre",
             "kg/m3": "KilogramPerCubicMetre", "g/cm3": "GramPerCubicCentimetre",
             "kg/m2": "KilogramPerSquareMetre", "mg/cm2": "MilligramPerSquareCentimetre",
             "Ah/kg": "AmpereHourPerKilogram", "mAh/g": "MilliampereHourPerGram",
             "Ah": "AmpereHour", "mAh": "MilliampereHour",
             "Ah/m2": "AmpereHourPerSquareMetre", "mAh/cm2": "MilliampereHourPerSquareCentimetre",
             "Wh": "WattHour", "mWh": "MilliwattHour", 
             "Wh/kg": "WattHourPerKilogram",
             "Wh/L": "WattHourPerLitre", 
             "mol/L": "MolePerLitre", "mol/m3": "MolePerCubicMetre",
             "mol/kg": "MolePerKilogram",
             "mass fraction": "MassFractionUnit", 
             "V": "Volt", "mV": "Millivolt",
             "A": "Ampere", "mA": "Milliampere", 
             "s": "Second", "min": "Minute", "h": "Hour"}

material_prefLabel = {"LFP" : "LithiumIronPhosphate", 
                      "LCO": "LithiumCobaltOxide",
                      "NCA": "LithiumNickelCobaltAluminium",
                      "LNMO": "LithiumNickelManganeseOxide",
                      "LMO": "LithiumManganeseOxide",
                      "NMC": "LithiumNickelManganeseCobaltOxide",
                      "NMC111": "LithiumNickelManganeseCobalt111",
                      "NMC532": "LithiumNickelManganeseCobalt532",
                      "NMC622": "LithiumNickelManganeseCobalt622",
                      "NMC811": "LithiumNickelManganeseCobalt811",
                      "Graphite": "Graphite", 
                      "Si": "Silicon",
                      "Li": "Lithium",
                      "PVDF": "PolyvinylFluoride",
                      "CMC": "CarboxymethylCellulose",
                      "Carbon Black": "CarbonBlack",
                      "LiPF6": "LithiumHexafluorophosphate",
                      "LiTFSI": "LithiumBistriflimide",
                      "EC": "EthyleneCarbonate",
                      "EMC": "EthylmethylCarbonate",
                      "DEC": "DiethyleneCarbonate",
                      "DMC": "DimethylCarbonate",
                      "FEC": "FluoroethyleneCarbonate"}

material_abbreviations = flipped_dict = {v: k for k, v in material_prefLabel.items()}
unit_abbreviations = flipped_dict = {v: k for k, v in unit_prefLabel.items()}

label_dict = {**label_uri_dict, **uri_label_dict, **unit_prefLabel, **unit_abbreviations, **material_prefLabel, **material_abbreviations}


json_g = upload_files(g)
# if json_g is not None:
#     for s, p, o in json_g:
#         st.write(s, p, o)

cell_iri = get_cell_iri(json_g)
dict = get_data(json_g, cell_iri, label_dict)

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
    df = download_dataset(dict["accessURL"])
    col1, col2 = st.columns(2)
    with col1:
        # Display the DataFrame in Streamlit
        if st.checkbox("View Data Table"):
            st.write(df)
    with col2:
        plot= st.checkbox("Plot Data")
            
    if plot:
        plot_time_voltage(json_g, dict["datasets"], df)
    


with st.expander("References"):
    st.text_input("Reference", value=dict["reference"], disabled=True)