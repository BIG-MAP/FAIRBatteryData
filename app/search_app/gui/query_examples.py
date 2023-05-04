battery_cell = "battery_68ed592a_7924_45d0_a108_94d6275d57f0"
ncm = "http://emmo.info/emmo#EMMO_4950a41c_ae32_4ce9_9db9_0076bbcac18f"



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

query1 = PREFIXES  + """
SELECT ?instance
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0.
}
"""

query2 = PREFIXES  + """
SELECT ?instance
WHERE {
    ?instance rdfs:subClassOf echem:electrochemistry_10359c79_cdf2_401a_83ee_d22e7fbb2ad1.
}
"""

query_instance_connections = PREFIXES  + """

SELECT ?instance ?objprop ?literal
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
             ?objprop ?literal.
}
"""

query_selected_keys = PREFIXES  + """

SELECT ?cellname ?instance ?creator ?prodate 
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
             schema:creator ?creator;
             schema:productionDate ?prodate;
             schema:name ?cellname.
}
"""

query_deep_into_graph_0 = PREFIXES  + """

SELECT ?cellname ?instance ?cathodeam
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
              schema:name ?cellname;
              echem:electrochemistry_8e9cf965_9f92_46e8_b678_b50410ce3616 ?cathode.

              ?cathode (emmo:EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec)+ ?something.

              ?something rdf:type ?cathodeam.

              ?cathodeam rdfs:subClassOf emmo:EMMO_8a41ed1b_64f9_4be7_9b60_01fcece45075.

}
"""


query_deep_into_graph = PREFIXES  + """

SELECT ?cellname ?instance ?cathodeam ?anodeam 
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
              schema:name ?cellname;
              echem:electrochemistry_8e9cf965_9f92_46e8_b678_b50410ce3616 ?cathode;
              echem:electrochemistry_5d299271_3f68_494f_ab96_3db9acdd3138 ?anode.

              ?cathode (emmo:EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec)+ ?something.

              ?something rdf:type ?cathodeam.

              ?cathodeam rdfs:subClassOf emmo:EMMO_8a41ed1b_64f9_4be7_9b60_01fcece45075.

              ?anode(emmo:EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec)+ ?something_else.

              ?something_else rdf:type ?anodeam.

              ?anodeam rdfs:subClassOf emmo:EMMO_8a41ed1b_64f9_4be7_9b60_01fcece45075.
}
"""

query_all_materials = PREFIXES  + """

SELECT ?chemicalmaterial
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
              (echem:electrochemistry_8e9cf965_9f92_46e8_b678_b50410ce3616|echem:electrochemistry_5d299271_3f68_494f_ab96_3db9acdd3138) ?something.

    ?something (emmo:EMMO_dba27ca1_33c9_4443_a912_1519ce4c39ec)+ ?material.
    ?material rdf:type ?chemicalmaterial.

    ?chemicalmaterial rdfs:subClassOf emmo:EMMO_8a41ed1b_64f9_4be7_9b60_01fcece45075.
}
"""

query_all_creators = PREFIXES  + """

SELECT ?creator
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
              schema:creator ?creator.
}
"""

query_all_dates = PREFIXES  + """

SELECT ?date
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
              schema:productionDate ?date.
}
"""

query_all_manufacturers = PREFIXES  + """

SELECT ?manufacturer
WHERE {
    ?instance rdf:type battery:battery_68ed592a_7924_45d0_a108_94d6275d57f0;
              schema:manufacturer ?manufacturer.
}
"""