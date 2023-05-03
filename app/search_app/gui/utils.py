
from rdflib import Graph, SKOS, Literal, URIRef, RDF
import warnings



PATH_JSONLD = "../ontologies/scientific_metadata.json"

######################################
# IRIs and PREF LABELS
######################################

def iri_to_preflabel(rdf_graph:Graph, iri:str)-> str:
    """
    Queries the triplestore for the IRI supplied, and retrievies its prefLabel if it exists.

    rdf_graph: RDFLib Graph object.
    iri: IRI of the enetity.

    """

    # (IRI hasPrefLabel prefLable)
    prefLabel = list(rdf_graph.objects(subject=URIRef(iri), predicate=SKOS.prefLabel))

    if len(prefLabel) == 1:
        return prefLabel[0].value

    else:
        warnings.warn(f"""The supplied IRI {iri} has {len(list(prefLabel))} prefLabels: {list(prefLabel)}""")
        return ""



def preflabel_to_iri(rdf_graph:Graph, prefLabel:str, lang:str=None) -> str:
    """
    Queries the triplestore for the prefLable supplied, and retrievies its IRI if it exists.

    rdf_graph: RDFLib Graph object.
    prefLabel: The prefLabel of the entity
    """

    # TODO: What if lang is no? or is it always en?
    if not lang:
        prefLabel_literal = Literal(prefLabel)
    else:
        prefLabel_literal = Literal(prefLabel, lang='en')

    # Make a list of all IRIs with the prefLabel
    iri = list(rdf_graph.subjects(predicate=SKOS.prefLabel, object=prefLabel_literal))

    if len(list(iri)) == 1:
        return str(iri[0])
    else:
        warnings.warn(f"""The supplied prefLabel {prefLabel} 
                         has {len(list(iri))} IRIs: {list(iri)}. Try adding the parameter lang=en""")
        return ""





def all_IRIs(rdf_graph:Graph) -> dict:
    """
    Returns a dictionary with all prefLabel:IRI pairs in the triplestore.
    """

    iris_dict = {str(iri):str(label) for iri, label in rdf_graph.subject_objects(predicate=SKOS.prefLabel)}
 
    return iris_dict


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
    



#################################
#   ABSTRACTED FUNCTIONS
################################

def get_all_ld_types():
    g, label_uri_dict, uri_label_dict = load_ontologies()
    metadata_graph = Graph().parse(PATH_JSONLD)
    types_dict = all_types(uri_label_dict, metadata_graph)
    return types_dict