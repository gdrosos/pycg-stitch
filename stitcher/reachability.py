import networkx as nx
import matplotlib.pyplot as plt
from stitcher.node import Node
import json
import pprint


class ReachabilityDetector:
    def __init__(self, callgraph, coordinate):
        self.nodes = set(callgraph["nodes"].keys())
        self.callgraph = callgraph
        self.root_package,  self.root_version = coordinate.split(":")
        self.visited_nodes = set()
        self.metrics = {}
        
        self.graph = self._load_to_networkx(callgraph)
        self.reach_all_nodes()
        self.extract_metrics()
        self.draw()

    
    def draw(self):
        node_labels = nx.get_node_attributes(self.graph,'URI')
        pos = nx.spring_layout(self.graph, scale=6)
        nx.draw(self.graph, pos, with_labels=False)
        nx.draw_networkx_labels(self.graph, pos, labels = node_labels)
        plt.show()

    def _load_to_networkx(self, callgraph):
        graph = nx.DiGraph()
        for node in callgraph["nodes"]:
            graph.add_node(node, URI=callgraph["nodes"][node]["URI"])
        for edge in callgraph["edges"]:
            graph.add_edge(edge[0], edge[1])
        return graph

    def reach_all_nodes(self):
        entrypoints = self.find_entrypoints()
        for node in entrypoints:
            nodes = nx.descendants(self.graph ,node)
            self.visited_nodes.update(nodes)
            self.visited_nodes.add(node)
    
    def find_entrypoints(self):
        entrypoints=set()
        for item in self.callgraph["nodes"]:
            node = Node(self.callgraph["nodes"][item]["URI"])
            if node.get_product()== self.root_package:
                entrypoints.add(item)
        return [x for x in entrypoints if  self.graph.in_degree(x)==0]

    
    def extract_metrics(self):
        self.metrics["product"] = self.root_package
        self.metrics["version"] = self.root_version
        self.metrics["total_nodes"] = len(self.nodes)
        self.metrics["visited_nodes"] = len(self.visited_nodes)
        # pprint.pprint(self.metrics)
