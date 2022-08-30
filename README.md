# FAIRBatteryData
This repository demonstrates a working proof-of-concept for how the Battery Interface Ontology (BattINFO) can be used to create semantically annotated battery data. Achieving this objective means developing not only the ontology itself, but also the associated data models and RDF triple mapping and querying infrastructure needed to perform practical actions on real battery datasets. In this first use-case, we create battery cell metadata for a cell that has been reported in the literature and link it with simulated time-series data obtained from the open-source Battery Modelling Toolbox (BattMo). The resulting metadata are mapped to BattINFO terms using RDF triples and saved in a triplestore. We demonstrate a simple semantic query of the triplestore using SPARQL.

The aim of this demonstration is to annotate cell-level and time-series battery data with BattINFO. Annotating data to ontology terms is achieved by defining semantic RDF triples, which take the form: subject, predicate, object. While in this case the subject and the predicate can be obtained from the relevant ontologies, we need an adequate data model to serve as a basis for identifying the object of the triple. We achieve this by creating instances in DLite. DLite instances are simple metadata that can be linked to or generated from ontologies. They provide property fields that can be populated with data coming from standard sources such as csv, xlsx, json, or data bases like Postgresql, etc. A conceptual overview of the layers linking raw data to ontology terms is presented in the following figure.


![image](https://user-images.githubusercontent.com/52653938/187467697-2d9025ea-8693-43d4-b242-bb248ace6849.png)

# Requirements
## Battery Interface Ontology (BattINFO)
BattINFO is a free, open-source domain ontology for batteries developed beneath the umbrella of the top-level EMMO. It is available for download on github, using the following link: https://github.com/BIG-MAP/BattINFO In this case study, we are working with version 0.3.0. The domain ontology can be obtained by cloning the git repo using the command:

`git clone https://github.com/BIG-MAP/BattINFO.git`

There are two tools we recommend to explore and use the ontology. The first is the free tool Protégé, developed by Stanford University. Protégé, provides an easy-to-use interface to explore and edit terms in the ontology. It is available for download using the following link: https://protege.stanford.edu/products.php#desktop-protege 
<br>
The second tool we recommend is a python package for working with EMMO and its associated domain ontologies called EMMOntoPy. It can be installed using the following command: <br>
`pip install EMMOntoPy` 

## DLite
To create mappings between ontological terms and actual data sets, we use a lightweight data-centric framework for semantic interoperability called DLite. DLite is a C implementation of the SINTEF Open Framework and Tools (SOFT), which is a set of concepts and tools for how to efficiently describe and work with scientific data.
If you are using Python, the easiest way to install DLite is with pip: <br>

`pip install DLite-Python`

Note, currently only Linux versions for Python 3.7, 3.8, 3.9 and 3.10 are available. But Windows versions will soon be available.
