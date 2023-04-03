import streamlit as st
import pandas as pd
import numpy as np
from pyvis.network import Network
import networkx as nx
import graphviz
import networkx as nx
import plotly.graph_objects as go
from pathlib import Path
import os
import streamlit_ace
import re

import plotly.express as px


import rdflib

import networkx as nx

from bokeh.models import Circle, MultiLine
from bokeh.plotting import figure, from_networkx, show
from collections import defaultdict
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, RDFS, SKOS
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
from rdflib.plugins.sparql import prepareQuery

import pandas as pd
import requests

def load_ontology():
    emmo = 'https://emmo-repo.github.io/versions/1.0.0-beta3/emmo-inferred.ttl'
    quantities = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/isq_bigmap_temp.ttl'
    cs = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/computerscience_bigmap_temp.ttl'
    electrochemical_quantities = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/electrochemicalquantities.ttl'
    electrochemistry = 'https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/electrochemistry.ttl'
    battery_quantities = 'https://raw.githubusercontent.com/emmo-repo/domain-battery/master/batteryquantities.ttl'
    battery = 'https://raw.githubusercontent.com/emmo-repo/domain-battery/master/battery.ttl'

    kg_path_mod = 'https://raw.githubusercontent.com/BIG-MAP/FAIRBatteryData/json-ld/app/kg-battery-mod.ttl'
    experts = 'https://raw.githubusercontent.com/BIG-MAP/FAIRBatteryData/json-ld/app/BatteryExperts.ttl'

    g= Graph()
    g.parse(emmo, format='ttl')
    g.parse(quantities, format='ttl')
    g.parse(cs, format='ttl')
    g.parse(electrochemical_quantities, format='ttl')
    g.parse(electrochemistry, format='ttl')
    g.parse(battery_quantities, format='ttl')
    g.parse(battery, format='ttl')
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


st.title('FAIR Battery Data Demo')

g, label_uri_dict, uri_label_dict = load_ontology()

st.write(label_uri_dict['SimonClark'])

thisdir = Path(__file__).resolve().parent 
knowledgedir = thisdir

kg_path_mod = f"{knowledgedir}/kg-battery-mod.ttl"

# Load RDF graph from a file
graph = rdflib.Graph()
graph.parse(kg_path_mod, format="ttl")

def extract_pref_labels(g):
    pref_labels = {}
    for s, p, o in g:
        if not isinstance(o, rdflib.term.Literal):
            continue
        if p == rdflib.term.URIRef(SKOS.prefLabel):
            pref_labels[str(s)] = str(o)
    return pref_labels

prefLabels = extract_pref_labels(graph)
st.write(prefLabels.values())
#st.write(uri_label_dict.keys())

# Define the graph visualization
nodes = []
edges = []
seen_nodes = set()

for s, p, o in graph:
    source = str(s)
    target = str(o)
    predicate = str(p)
    if isinstance(o, URIRef) and target not in seen_nodes:
        if target in uri_label_dict.keys():
            node_label = uri_label_dict[target]
        else:
            node_label = ""
        
        nodes.append(Node(id = target, label = node_label))
        seen_nodes.add(target)
    if source not in seen_nodes:
        if source in uri_label_dict:
            node_label = uri_label_dict[source]
        else:
            node_label = ""
        
        nodes.append(Node(id = source, label = node_label))
        seen_nodes.add(source)
    
    if predicate in uri_label_dict:
        edge_label = uri_label_dict[predicate]
    else:
        edge_label = re.search(r'#(\w+)', predicate).group(1)
    edges.append( Edge( source=source, target = target, label = edge_label))


config = Config(width=750,
                height=950,
                directed=True, 
                physics=True, 
                hierarchical=False,
                # **kwargs
                )

ag = agraph(nodes=nodes, edges=edges, config=config)

# node_dict = {n.id: n for n in nodes}
# selected_node_id = st.selectbox("Select a node", options=node_dict)

# # Render the graph
# nodes = []
# edges = []
# seen_nodes = set()

# for s, p, o in graph:
#     source = str(s)
#     target = str(o)
#     if isinstance(o, URIRef) and target not in seen_nodes and target == selected_node_id:
#         nodes.append(Node(id = target))
#         seen_nodes.add(target)
#     if source not in seen_nodes and source == selected_node_id:
#         nodes.append(Node(id = source))
#         seen_nodes.add(source)
#     edges.append( Edge( source=source, target = target))

# selected_node = nodes



# for edge in edges:
#     #st.write(dir(edge))
#     st.write(edge.to)
#     if edge.to == selected_node:
#         st.write("selected node is target")
#         nodes.append(edge.source)
#     elif edge.source == selected_node:
#         st.write("selected node is source")
#         nodes.append(edge.to)

# st.write(nodes)
# st.write(edges)

# # node_dict = {n.id: n for n in nodes}
# # seen_nodes = set()
# # selected_node_id = st.selectbox("Select a node", options=node_dict)
# # selected_node = [n for n in nodes if n.id == selected_node_id][0]
# # st.write(selected_node)
# # seen_nodes.add(selected_node)


# # selected_edges = [e for e in edges if e.source == selected_node]
# # for edge in edges:
# #     #st.write(dir(edge))
# #     if edge.to == selected_node:
# #         selected_edges.append(edge)

# # selected_nodes = [Node(selected_node)]
# # for edge in selected_edges:
# #     target_node = Node(edge.to)
# #     if target_node not in seen_nodes:
# #         selected_nodes.append(target_node)
# #         seen_nodes.add(target_node)
    
    
# # agraph(nodes=selected_nodes, edges=selected_edges, config=config)

# agraph(nodes=nodes, edges=edges, config=config)

st.subheader('Accessible')

# Set the URL for the CSV file
url = "https://raw.githubusercontent.com/BIG-MAP/OntologyExercises/main/data/TeamB.csv"

# Use Pandas to read the CSV data
data = pd.read_csv(url)

# Display the data in Streamlit
st.write(data)

# Select the columns you want to plot
selected_columns = st.multiselect('Select columns to plot', data.columns)

# Filter the data to only include the selected columns
data = data[selected_columns]

# Create a line chart using Plotly
fig = px.line(data, x=data.index, y=data.columns, title='Line Chart')

# Display the chart in Streamlit
st.plotly_chart(fig)

st.subheader('Interoperable')

st.subheader('Reusable')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')



# g = Network(height=800, width = 800, notebook=True)
# g.toggle_hide_edges_on_drag(True)
# g.barnes_hut()
# g.from_nx(nx.davis_southern_women_graph())
# g.show("ex.html")

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

st.subheader('Graph Section')




G = nx.karate_club_graph()

SAME_CLUB_COLOR, DIFFERENT_CLUB_COLOR = "darkgrey", "red"

edge_attrs = {}
for start_node, end_node, _ in G.edges(data=True):
    edge_color = SAME_CLUB_COLOR if G.nodes[start_node]["club"] == G.nodes[end_node]["club"] else DIFFERENT_CLUB_COLOR
    edge_attrs[(start_node, end_node)] = edge_color

nx.set_edge_attributes(G, edge_attrs, "edge_color")

plot = figure(width=400, height=400, x_range=(-1.2, 1.2), y_range=(-1.2, 1.2),
              x_axis_location=None, y_axis_location=None, toolbar_location=None,
              title="Graph Interaction Demo", background_fill_color="#efefef",
              tooltips="index: @index, club: @club")
plot.grid.grid_line_color = None

graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="lightblue")
graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color",
                                               line_alpha=0.8, line_width=1.5)
plot.renderers.append(graph_renderer)
plot.background_fill_color = 'black'

st.bokeh_chart(plot)

st.subheader('Another Network Graph Chart')


thisdir = Path(__file__).resolve().parent
knowledgedir = thisdir

kg_path_mod = f"{knowledgedir}/kg-battery-mod.ttl"

# Load RDF graph from a file
graph = rdflib.Graph()
graph.parse(kg_path_mod, format="ttl")

# Create a networkx graph from the RDF graph
nx_graph = nx.Graph()

for subject, predicate, object in graph:
    nx_graph.add_edge(subject, object)

# Generate the node labels using the skos:prefLabel property
node_labels = defaultdict(str)
for subject, predicate, object in graph.triples((None, rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#prefLabel'), None)):
    node_labels[subject] = str(object)


pos = nx.spring_layout(nx_graph)
nx.draw_networkx_nodes(nx_graph, pos, node_size=100, node_color='lightblue')
nx.draw_networkx_edges(nx_graph, pos)
nx.draw_networkx_labels(nx_graph, pos, labels=node_labels, font_size=10, font_family="Arial")

st.pyplot()


st.subheader('A plotly example')
pos = nx.spring_layout(nx_graph, seed=42)

# Create edges trace
edge_x = []
edge_y = []
for edge in nx_graph.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='gray'), mode='lines')

# Create nodes trace
node_x = []
node_y = []
node_text = []
for node in pos:
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node_labels[node])

node_trace = go.Scatter(
    x=node_x, y=node_y,
    text=node_text, 
    mode='markers+text', 
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

fig = go.Figure(data=[edge_trace, node_trace],
              layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

st.plotly_chart(fig)