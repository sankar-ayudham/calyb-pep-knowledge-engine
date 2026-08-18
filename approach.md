# Project Approach & Architectural Notes

## Domain Selection & Scope
I chose **Domain A: Language Evolution**, specifically focusing on the Python type hinting ecosystem (PEPs 484, 526, 544, and 589). 

This subset was selected because type annotations represent one of the most debated language additions in Python's history. It has clear lineage (PEP 526 and 589 build directly on PEP 484) and explicitly documents "Rejected Ideas" (e.g., prohibiting runtime type enforcement).

## Entity and Relationship Schema
The knowledge base is built as a Directed Graph using custom schema entities:

### Entities
- `PEPNode`: Captures proposal metadata (title, PEP number).
- `FeatureNode`: Captures specifications introduced by a PEP.
- `RejectedIdeaNode`: Captures mechanics that were explicitly considered and rejected.

### Relationships
- `REQUIRES`: Predecessor/dependency relationships between PEPs.
- `INTRODUCES`: Connects a PEP to its core technical features.
- `REJECTS_ALTERNATIVE`: Connects a PEP to its rejected design ideas.

*Note: In accordance with the assignment constraint, entity and relationship mapping was implemented manually using regular expression pattern matching on ReStructuredText headers in `src/parser.py` without external extraction frameworks.*

## Knowledge Representation & Storage
The network is maintained in memory via NetworkX and exported to `data/knowledge_state.json`. This provides an auditable, human-readable snapshot of all nodes and directed links.

## Proposal Reasoning
When a new feature proposal is evaluated via CLI:
1. Key terms are extracted from the user's input.
2. The reasoner searches the graph for matching entities and traverses predecessor links to find related PEPs and historical rejections.
3. It constructs an evaluation summary detailing related prior art and flagging potential conflicts with past design decisions.

## Future Scope
- **Semantic Matching:** Replace simple token searching with local vector embeddings (e.g., `sentence-transformers`) to handle semantic equivalents (e.g., mapping "enforce types during execution" to "runtime validation").
- **Extended PEP Lineage:** Extend parsing to cover typing additions up to PEP 604/646.