import string


class ProposalReasoner:
    def __init__(self, kg_manager):
        self.kg = kg_manager
        self.ignore_words = {"i", "want", "to", "add", "a", "the", "in", "for", "with", "is", "of", "and", "that",
                             "should"}

    def _tokenize(self, text: str) -> list:
        clean = text.lower().translate(str.maketrans('', '', string.punctuation))
        return [w for w in clean.split() if w not in self.ignore_words and len(w) > 2]

    def evaluate(self, proposal_text: str) -> str:
        tokens = self._tokenize(proposal_text)
        context = self.kg.query_related_context(tokens)

        lines = []
        lines.append("PROPOSAL EVALUATION REPORT")
        lines.append("==========================")
        lines.append(f"Input: \"{proposal_text}\"\n")

        lines.append("1. Extracted Key Concepts:")
        lines.append(f"   {', '.join(tokens) if tokens else 'None'}\n")

        lines.append("2. Relevant Prior Art & Standards:")
        if context["peps"]:
            for pep in context["peps"]:
                lines.append(f"   - {pep}")
        else:
            lines.append("   - No direct overlap identified in baseline PEP set.")
        lines.append("")

        lines.append("3. Conflict & Risk Assessment (Historical Rejections):")
        if context["rejections"]:
            lines.append("   [WARNING] This proposal touches mechanisms previously rejected:")
            for rej in context["rejections"]:
                lines.append(f"   * {rej}")
        else:
            lines.append("   - No direct conflicts found with historical rejections.")
        lines.append("")

        lines.append("4. Recommendation:")
        if context["rejections"]:
            lines.append(
                "   -> Review historical objections above and address runtime performance constraints before drafting a formal proposal.")
        else:
            lines.append(
                "   -> Idea appears novel relative to current knowledge base. Proceed with pre-PEP community feedback.")

        return "\n".join(lines)