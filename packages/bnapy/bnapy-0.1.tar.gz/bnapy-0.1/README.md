# BNApy (Bipartite Network Analysis)

BNA is a Python package for analyzing and visualizing bipartite network data at multiple levels: individual, dyad, mesoscale, and group-level interactions. It includes methods to quantify individual interaction patterns, identify statistically significant dyadic relationships, detect mesoscale structures via clustering, and visualize networks with an emphasis on user interaction and metadata inclusion.

## Features

- **Individual-level Analysis**: Compute node-level measures such as quantity and diversity of interactions.
- **Dyadic Analysis**: Identify statistically significant edges in the interaction network using null models.
- **Mesoscale Clustering**: Automatically detect the number of clusters in a bipartite network using clustering methods.
- **Visualization**: Generate interactive visualizations (including Sankey diagrams) and visualize bipartite networks at group and cohort levels.
- **Web Interface**: Includes a web-based interface for engaging with the visualizations.
- **Extensibility**: Easily incorporate additional measures, clustering methods, or visualizations.

## Installation

To install BNA, you can use `pip` from the PyPI repository:

```bash
pip install bna

BNA_Package/
├── __init__.py
├── individual/
│   ├── __init__.py
│   ├── quantity_diversity.py    
│   └── tests/                   
│       ├── __init__.py
│       └── test_quantity_diversity.py
├── dyad/
│   ├── __init__.py
│   ├── significant_edges.py     
│   └── tests/                  
│       ├── __init__.py
│       └── test_significant_edges.py
├── mesoscale/
│   ├── __init__.py
│   ├── clustering.py            
│   └── tests/                  
│       ├── __init__.py
│       └── test_clustering.py
├── visualization/
│   ├── __init__.py
│   ├── network_visualization.py 
│   ├── web_interface.py         
│   └── tests/                   
│       ├── __init__.py
│       └── test_network_visualization.py
├── utils/
│   ├── __init__.py
│   ├── graph_tools.py        
│   ├── plot_tools.py          
│   └── tests/
│       ├── __init__.py
│       ├── test_graph_tools.py
│       └── test_plot_tools.py
├── data/                       
    ├── __init__.py
    └── synthetic_data.csv
