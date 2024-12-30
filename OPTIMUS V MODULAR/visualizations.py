import networkx as nx
import matplotlib.pyplot as plt
import random

# Define a function to initialize the graph with nodes and edges
def initialize_graph():
    """Initialize the directed graph with institutions and basic properties."""
    G = nx.DiGraph()

    # Define nodes with properties
    nodes = {
        "Parliament": {"color": "skyblue", "size": 1200},
        "Government": {"color": "lightgreen", "size": 1200},
        "Judiciary": {"color": "orange", "size": 1200},
        "Citizen Pressure": {"color": "salmon", "size": 1200},
        "Norm": {"color": "purple", "size": 1000},
        "Law": {"color": "lightcoral", "size": 1000},
        "Regulation": {"color": "gold", "size": 1000},
    }

    # Add nodes with properties to the graph
    for node, attributes in nodes.items():
        G.add_node(node, color=attributes["color"], size=attributes["size"])

    # Define edges representing structural couplings and interactions
    edges = [
        ("Parliament", "Law"),            # Parliament enacts laws
        ("Government", "Regulation"),     # Government enacts regulations
        ("Law", "Judiciary"),             # Laws are tested by the judiciary
        ("Regulation", "Judiciary"),      # Regulations are tested by the judiciary
        ("Citizen Pressure", "Government"),  # Citizens pressure government decisions
        ("Judiciary", "Norm"),            # Judiciary evaluates norms
        ("Norm", "Citizen Pressure"),     # Norms influence citizens
    ]

    # Add edges to the graph
    G.add_edges_from(edges)
    return G

# Define a function to update node sizes based on dynamic data (e.g., citizen pressure level)
def update_node_sizes(G, dynamic_data):
    """Update node sizes based on dynamic data (e.g., citizen pressure or caseloads)."""
    for node, data in dynamic_data.items():
        if node in G.nodes:
            G.nodes[node]["size"] = data.get("size", G.nodes[node]["size"])

# Define a function to update edge colors or weights based on interactions
def update_edges(G, edge_updates):
    """Update edges based on external data or interactions (e.g., influence levels)."""
    for edge, properties in edge_updates.items():
        if G.has_edge(*edge):
            G.edges[edge].update(properties)

# Define the visualization function
def visualize_graph(G):
    """Draw the graph with current node and edge properties."""
    pos = nx.spring_layout(G, seed=42)  # Use spring layout for a network-like structure

    # Extract color and size information for visualization
    node_colors = [G.nodes[node]["color"] for node in G.nodes]
    node_sizes = [G.nodes[node]["size"] for node in G.nodes]

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw(
        G, pos, 
        with_labels=True, 
        node_color=node_colors, 
        node_size=node_sizes, 
        edge_color="gray", 
        font_size=10, 
        font_weight="bold",
        arrows=True,
        arrowsize=20,
        arrowstyle='-|>'
    )

    plt.title("OPTIMUS Model - Institutional Interactions")
    plt.show()

# Example Usage
if __name__ == "__main__":
    # Initialize the graph
    G = initialize_graph()

    # Example dynamic data (for demonstration purposes, replace with real-time data)
    dynamic_data = {
        "Citizen Pressure": {"size": 1500},
        "Government": {"size": 1300}
    }
    update_node_sizes(G, dynamic_data)

    # Example edge update (e.g., from dynamic interaction levels)
    edge_updates = {
        ("Parliament", "Law"): {"color": "blue", "weight": 2},
        ("Government", "Regulation"): {"color": "green", "weight": 1.5}
    }
    update_edges(G, edge_updates)

    # Visualize the updated graph
    visualize_graph(G)