from __future__ import annotations

import uuid
from copy import deepcopy
from typing import Any


def gen_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class NormativeProfileBuilder:
    def build(
        self,
        enriched_doc: dict[str, Any],
        doc_role: str = "reference",
    ) -> dict[str, Any]:
        document = enriched_doc.get("document", {})
        enrichment = enriched_doc.get("enrichment", {})

        document_profile = enrichment.get("document_profile", {})
        style_profile = enrichment.get("style_profile", {})
        table_signatures = enrichment.get("table_signatures", [])
        field_candidates = enrichment.get("field_candidates", [])
        document_layout_type = enrichment.get("document_layout_type")
        text_units_stats = enrichment.get("text_units_stats", {})

        profile = {
            "normative_id": gen_id("norm"),
            "source_document_id": document.get("document_id"),
            "filename": document.get("filename"),
            "doc_role": doc_role,
            "title": document_profile.get("title"),
            "doc_type_candidate": None,
            "document_layout_type": document_layout_type,
            "text_units_stats": text_units_stats,
            "section_titles": document_profile.get("section_titles", []),
            "top_headings": document_profile.get("top_headings", []),
            "keywords": document_profile.get("keywords", []),
            "first_meaningful_texts": document_profile.get("first_meaningful_texts", []),
            "style_profile": deepcopy(style_profile),
            "table_signatures": deepcopy(table_signatures),
            "field_candidates": self._compact_field_candidates(field_candidates),
            "stats": {
                "sections_count": len(document_profile.get("section_titles", [])),
                "tables_count": len(table_signatures),
                "field_candidates_count": len(field_candidates),
            },
        }

        return profile

    def _compact_field_candidates(self, field_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        compact = []

        for item in field_candidates:
            compact.append({
                "field_name": item.get("field_name"),
                "field_value": item.get("field_value"),
                "is_empty_like": item.get("is_empty_like"),
                "source": item.get("source"),
                "anchor": item.get("anchor"),
            })

        return compact
    
# import json
# from document_enricher import DocumentEnricherV2
# from normative_profile_builder import NormativeProfileBuilder

# with open("parsed_sample_expanded2.json", "r", encoding="utf-8") as f:
#     parsed_doc = json.load(f)

# enricher = DocumentEnricherV2()
# enriched_doc = enricher.enrich(parsed_doc)

# builder = NormativeProfileBuilder()
# normative_profile = builder.build(enriched_doc, doc_role="reference")

# with open("normative_profile.json", "w", encoding="utf-8") as f:
#     json.dump(normative_profile, f, ensure_ascii=False, indent=2)