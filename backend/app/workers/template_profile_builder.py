from __future__ import annotations

import uuid
from copy import deepcopy
from typing import Any


def gen_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class TemplateProfileBuilder:
    def build(
        self,
        enriched_doc: dict[str, Any],
        doc_role: str = "template",
    ) -> dict[str, Any]:
        document = enriched_doc.get("document", {})
        enrichment = enriched_doc.get("enrichment", {})

        document_profile = enrichment.get("document_profile", {})
        style_profile = enrichment.get("style_profile", {})
        table_signatures = enrichment.get("table_signatures", [])
        field_candidates = enrichment.get("field_candidates", [])
        document_layout_type = enrichment.get("document_layout_type")
        text_units_stats = enrichment.get("text_units_stats", {})

        return {
            "template_id": gen_id("tpl") if doc_role == "template" else None,
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

    def _compact_field_candidates(self, field_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "field_name": item.get("field_name"),
                "field_value": item.get("field_value"),
                "is_empty_like": item.get("is_empty_like"),
                "source": item.get("source"),
                "anchor": item.get("anchor"),
            }
            for item in field_candidates
        ]