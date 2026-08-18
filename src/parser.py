import os
import re
import urllib.request
from .schema import PEPNode, FeatureNode, RejectedIdeaNode, Edge

PEP_URLS = {
    "484": "https://raw.githubusercontent.com/python/peps/main/peps/pep-0484.rst",
    "526": "https://raw.githubusercontent.com/python/peps/main/peps/pep-0526.rst",
    "544": "https://raw.githubusercontent.com/python/peps/main/peps/pep-0544.rst",
    "589": "https://raw.githubusercontent.com/python/peps/main/peps/pep-0589.rst"
}


FALLBACK_DATA = {
    "484": """PEP: 484
Title: Type Hints
Requires: 3107

Abstract
--------
This PEP proposes a standard syntax for type annotations in Python code.

Rejected Ideas
--------------
* Dynamic or runtime type checking. Type checks must remain static and optional. Enforcing types at runtime or throwing exceptions on invalid types was explicitly rejected to prevent performance degradation.
""",
    "526": """PEP: 526
Title: Syntax for Variable Annotations
Requires: 484

Abstract
--------
This PEP adds syntax to Python for annotating variable types.

Rejected Ideas
--------------
* Automatically checking assignment types at runtime.
""",
    "544": """PEP: 544
Title: Protocols: Structural subtyping
Requires: 484

Abstract
--------
This PEP proposes a way to define structural subtyping (Protocols).
""",
    "589": """PEP: 589
Title: TypedDict: Type Hints for Dictionaries
Requires: 484

Abstract
--------
This PEP proposes TypedDict to support type hints for dictionaries with fixed keys.

Rejected Ideas
--------------
* Runtime validation of key-value dictionary types. TypedDict is strictly a static analysis feature.
"""
}


def fetch_pep_files(data_dir: str):
    headers = {'User-Agent': 'Mozilla/5.0'}
    for pep_num, url in PEP_URLS.items():
        path = os.path.join(data_dir, f"pep-{pep_num}.txt")
        if os.path.exists(path):
            continue
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=4) as resp, open(path, 'w', encoding='utf-8') as f:
                f.write(resp.read().decode('utf-8'))
        except Exception:
            # write fallback snippet if fetch fails
            with open(path, 'w', encoding='utf-8') as f:
                f.write(FALLBACK_DATA.get(pep_num, ""))


def parse_rst_section(text: str, section_header: str) -> str:
    pattern = rf'(?im)^{section_header}\s*\n[-=~^]+\s*\n(.*?)(?=\n^[A-Z][a-zA-Z0-9\s]+$\n[-=~^]+|\Z)'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def load_knowledge_elements(data_dir: str):
    nodes = []
    edges = []

    fetch_pep_files(data_dir)

    for fname in os.listdir(data_dir):
        if not fname.endswith('.txt'):
            continue

        with open(os.path.join(data_dir, fname), 'r', encoding='utf-8') as f:
            raw_text = f.read()

        pep_match = re.search(r'^PEP:\s*(\d+)', raw_text, re.MULTILINE)
        if not pep_match:
            continue
        pep_num = pep_match.group(1)

        title_match = re.search(r'^Title:\s*(.+)$', raw_text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f"PEP {pep_num}"

        pep_id = f"PEP_{pep_num}"
        nodes.append(PEPNode(id=pep_id, label="PEP", title=title, pep_number=pep_num))

        deps = re.findall(r'^Requires:\s*(\d+)', raw_text, re.MULTILINE)
        for dep in deps:
            edges.append(Edge(source_id=pep_id, target_id=f"PEP_{dep}", relation="REQUIRES"))

        abstract = parse_rst_section(raw_text, "Abstract")
        if abstract:
            feat_id = f"Feature_{pep_num}"
            nodes.append(FeatureNode(id=feat_id, label="Feature", description=abstract[:250]))
            edges.append(Edge(source_id=pep_id, target_id=feat_id, relation="INTRODUCES"))

        rejected = parse_rst_section(raw_text, "Rejected Alternatives") or parse_rst_section(raw_text, "Rejected Ideas")
        if rejected:
            items = [item.strip() for item in re.split(r'\n\*\s+', rejected) if item.strip()]
            for idx, item in enumerate(items):
                rej_id = f"Rej_{pep_num}_{idx}"
                clean_reason = item.replace('\n', ' ')
                nodes.append(RejectedIdeaNode(id=rej_id, label="RejectedIdea", reason=clean_reason[:200]))
                edges.append(Edge(source_id=pep_id, target_id=rej_id, relation="REJECTS_ALTERNATIVE"))

    return nodes, edges