from dataclasses import dataclass

@dataclass
class Node:
    id: str
    label: str

@dataclass
class PEPNode(Node):
    title: str
    pep_number: str

@dataclass
class FeatureNode(Node):
    description: str

@dataclass
class RejectedIdeaNode(Node):
    reason: str

@dataclass
class Edge:
    source_id: str
    target_id: str
    relation: str