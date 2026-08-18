import json
import networkx as nx


class KnowledgeGraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_from_elements(self, nodes, edges):
        for n in nodes:
            self.graph.add_node(n.id, **n.__dict__)
        for e in edges:
            self.graph.add_edge(e.source_id, e.target_id, relation=e.relation)

    def export_state(self, path: str):
        data = nx.node_link_data(self.graph, edges="links")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_state(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.graph = nx.node_link_graph(data, edges="links")

    def query_related_context(self, keywords: list) -> dict:
        matched_peps = set()
        matched_rejections = set()

        for node_id, attrs in self.graph.nodes(data=True):
            attr_text = " ".join(str(v) for v in attrs.values()).lower()
            if any(kw in attr_text for kw in keywords):
                if attrs.get('label') == 'PEP':
                    matched_peps.add(attrs.get('title'))
                elif attrs.get('label') == 'RejectedIdea':
                    matched_rejections.add(attrs.get('reason'))

                    for pred in self.graph.predecessors(node_id):
                        if self.graph.nodes[pred].get('label') == 'PEP':
                            matched_peps.add(self.graph.nodes[pred].get('title'))

        return {
            "peps": list(matched_peps),
            "rejections": list(matched_rejections)
        }