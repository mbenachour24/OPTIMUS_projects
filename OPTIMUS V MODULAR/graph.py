import networkx as nx
import matplotlib.pyplot as plt

class OptimusGraph:
    def __init__(self):
        self.graph = nx.DiGraph()  # Directed graph for structured, directional relationships
        self.create_nodes()
        self.create_edges()

    def create_nodes(self):
        # Defining core functional units as nodes with distinct attributes
        nodes = {
            "Judiciary": {"color": "lightblue", "size": 1800, "label": "Autopoiesis: Valid/Invalid"},
            "Legislature": {"color": "lightgreen", "size": 1800, "label": "Autopoiesis: Legal/Illegal"},
            "Executive": {"color": "lightcoral", "size": 1800, "label": "Autopoiesis: Enforceable/Unenforceable"},
            "Political System": {"color": "orange", "size": 1800, "label": "Autopoiesis: Legitimate/Illegitimate"},
            "Economy": {"color": "lightgrey", "size": 1800, "label": "Autopoiesis: Profitable/Unprofitable"},
            "Society": {"color": "yellow", "size": 2000, "label": "Central Orchestrator"},
            "Norms": {"color": "lightpink", "size": 1500, "label": "Guiding Principles"}
        }
        
        for node, attributes in nodes.items():
            self.graph.add_node(node, **attributes)

    def create_edges(self):
        # Defining relationships (edges) to show structural coupling between units
        edges = [
            ("Judiciary", "Legislature"),  # Legal system informs legislative actions
            ("Legislature", "Executive"),  # Laws created by legislature guide executive actions
            ("Executive", "Political System"),  # Executive decisions impact the political system
            ("Political System", "Society"),  # Political legitimacy monitored by society
            ("Society", "Norms"),  # Society establishes and maintains guiding norms
            ("Norms", "Judiciary"),  # Norms influence judiciary decisions
            ("Economy", "Society"),  # Economic output feeds into societal well-being
            ("Society", "Economy"),  # Society's needs influence economic structures
            ("Economy", "Political System")  # Economy influences political stability
        ]
        
        for edge in edges:
            self.graph.add_edge(*edge, weight=2)  # Weighted for visibility

    def draw_graph(self):
        # Layout designed to centralize 'Society' as orchestrator
        pos = nx.spring_layout(self.graph, seed=42, k=0.5)  # Adjusted for stability

        # Draw nodes with colors, sizes, and autopoietic labels
        colors = [self.graph.nodes[node]["color"] for node in self.graph.nodes]
        sizes = [self.graph.nodes[node]["size"] for node in self.graph.nodes]

        nx.draw(
            self.graph, pos, node_color=colors, node_size=sizes,
            with_labels=True, labels={node: node for node in self.graph.nodes},
            font_weight="bold", font_size=10, edge_color="gray", width=1.5
        )

        # Adding labels that represent each unit's autopoietic logic
        for node, (x, y) in pos.items():
            plt.text(
                x, y - 0.1, self.graph.nodes[node]["label"], fontsize=8, ha='center', 
                color="black", style="italic"
            )

        # Display the graph with title
        plt.title("Optimus System Graph: Functional Differentiation and Structural Coupling")
        plt.show()

# Run the graph visualization
if __name__ == "__main__":
    og = OptimusGraph()
    og.draw_graph()
