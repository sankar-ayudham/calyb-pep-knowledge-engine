import argparse
import os
from src.parser import load_knowledge_elements
from src.graph import KnowledgeGraphManager
from src.reasoner import ProposalReasoner

DATA_DIR = "data/raw_peps"
STATE_FILE = "data/knowledge_state.json"


def setup_knowledge_base():
    os.makedirs(DATA_DIR, exist_ok=True)

    print("Loading data and mapping schema...")
    nodes, edges = load_knowledge_elements(DATA_DIR)

    kg = KnowledgeGraphManager()
    kg.build_from_elements(nodes, edges)
    kg.export_state(STATE_FILE)
    print(f"Serialized graph state to {STATE_FILE}")
    return kg


def main():
    parser = argparse.ArgumentParser(description="PEP Knowledge Graph CLI")
    parser.add_argument("--proposal", type=str, help="Language feature proposal text to evaluate")
    args = parser.parse_args()

    kg = KnowledgeGraphManager()
    if not os.path.exists(STATE_FILE):
        kg = setup_knowledge_base()
    else:
        kg.load_state(STATE_FILE)

    if args.proposal:
        reasoner = ProposalReasoner(kg)
        report = reasoner.evaluate(args.proposal)
        print("\n" + report)
    else:
        print("Knowledge base ready. Run with --proposal \"<text>\" to evaluate an idea.")


if __name__ == "__main__":
    main()