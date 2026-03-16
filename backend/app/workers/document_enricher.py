from __future__ import annotations

import re
from collections import Counter
from copy import deepcopy
from typing import Any


STOPWORDS_RU = {
    "и", "в", "во", "на", "по", "с", "со", "для", "к", "ко", "о", "об", "от",
    "до", "из", "за", "под", "при", "над", "не", "что", "как", "или", "а",
    "но", "это", "то", "так", "у", "же", "ли", "бы", "быть", "является",
    "настоящий", "документ", "the", "and", "for", "with", "from", "this",
    "that", "www", "http", "https"
}


FIELD_PATTERNS = [
    re.compile(r"^\s*([A-Za-zА-Яа-яЁё0-9_\- /()№]+?)\s*:\s*(.+?)\s*$"),
    re.compile(r"^\s*([A-Za-zА-Яа-яЁё0-9_\- /()№]+?)\s*-\s*(.+?)\s*$"),
]


EMPTY_LIKE_PATTERNS = [
    re.compile(r"^_{2,}$"),
    re.compile(r"^\s*$"),
    re.compile(r"^<[^<>]{0,100}>$"),
    re.compile(r"^\[[^\[\]]{0,100}\]$"),
    re.compile(r"^\{\{[^{}]{0,100}\}\}$"),
    re.compile(r"^(указать|заполнить|fill in|to be filled)$", re.IGNORECASE),
]


def normalize_keyword_token(token: str) -> str:
    token = token.lower().strip()
    token = token.replace("ё", "е")
    return token


def extract_keywords_from_texts(texts: list[str], top_k: int = 20) -> list[str]:
    counter = Counter()

    for text in texts:
        tokens = re.findall(r"[A-Za-zА-Яа-яЁё0-9]{3,}", text.lower())
        for token in tokens:
            token = normalize_keyword_token(token)
            if token in STOPWORDS_RU:
                continue
            counter[token] += 1

    return [token for token, _ in counter.most_common(top_k)]


def most_common_non_null(values: list[Any]) -> Any:
    filtered = [v for v in values if v is not None]
    if not filtered:
        return None
    return Counter(filtered).most_common(1)[0][0]


def round_if_float(v: Any, digits: int = 1) -> Any:
    if isinstance(v, float):
        return round(v, digits)
    return v


def is_empty_like(value: str) -> bool:
    value = (value or "").strip()
    for pattern in EMPTY_LIKE_PATTERNS:
        if pattern.match(value):
            return True
    return False


def compact_text(text: str) -> str:
    text = text or ""
    text = re.sub(r"\s+", " ", text).strip()
    return text


class DocumentEnricherV2:
    def enrich(self, parsed_doc: dict[str, Any]) -> dict[str, Any]:
        enriched = deepcopy(parsed_doc)

        text_units = self._collect_text_units(parsed_doc)
        document_profile = self._build_document_profile(parsed_doc, text_units)
        style_profile = self._build_style_profile(text_units)
        field_candidates = self._extract_field_candidates(text_units, parsed_doc)
        table_signatures = self._build_table_signatures(parsed_doc.get("tables", []))
        layout_type = self._detect_document_layout_type(parsed_doc, text_units)

        enriched["enrichment"] = {
            "document_profile": document_profile,
            "style_profile": style_profile,
            "field_candidates": field_candidates,
            "table_signatures": table_signatures,
            "header_texts": [
                h.get("text", "")
                for h in parsed_doc.get("headers", [])
                if h.get("text")
            ],
            "footer_texts": [
                f.get("text", "")
                for f in parsed_doc.get("footers", [])
                if f.get("text")
            ],
            "text_units": text_units,
            "text_units_stats": {
                "total": len(text_units),
                "block_units": sum(1 for u in text_units if u["source"] == "block"),
                "table_cell_units": sum(1 for u in text_units if u["source"] == "table_cell_paragraph"),
            },
            "document_layout_type": layout_type,
        }

        return enriched

    # ---------------------------------------------------------
    # Text units
    # ---------------------------------------------------------

    def _collect_text_units(self, parsed_doc: dict[str, Any]) -> list[dict[str, Any]]:
        units: list[dict[str, Any]] = []

        # 1. Обычные blocks
        for block in parsed_doc.get("blocks", []):
            if block.get("block_type") not in {"paragraph", "heading"}:
                continue

            text = block.get("text_normalized") or ""
            if not compact_text(text):
                continue

            units.append({
                "unit_id": f"unit_block_{block.get('block_id')}",
                "source": "block",
                "block_id": block.get("block_id"),
                "table_id": None,
                "row_idx": None,
                "col_idx": None,
                "text": text,
                "style": block.get("style") or {},
                "paragraph_format": block.get("paragraph_format") or {},
                "runs": block.get("runs") or [],
                "block_type": block.get("block_type"),
                "section_path": block.get("section_path") or [],
                "anchor": {
                    "block_id": block.get("block_id")
                }
            })

        # 2. Paragraph внутри table cells
        for table in parsed_doc.get("tables", []):
            table_id = table.get("table_id")
            block_id = table.get("block_id")

            for cell in table.get("cells", []):
                row_idx = cell.get("row_idx")
                col_idx = cell.get("col_idx")

                for p_idx, p in enumerate(cell.get("paragraphs", [])):
                    text = p.get("text_normalized") or ""
                    if not compact_text(text):
                        continue

                    units.append({
                        "unit_id": f"unit_tbl_{table_id}_{row_idx}_{col_idx}_{p_idx}",
                        "source": "table_cell_paragraph",
                        "block_id": block_id,
                        "table_id": table_id,
                        "row_idx": row_idx,
                        "col_idx": col_idx,
                        "text": text,
                        "style": p.get("style") or {},
                        "paragraph_format": p.get("paragraph_format") or {},
                        "runs": p.get("runs") or [],
                        "block_type": "table_cell_paragraph",
                        "section_path": table.get("section_path") or [],
                        "anchor": {
                            "block_id": block_id,
                            "table_id": table_id,
                            "cell": {
                                "row_idx": row_idx,
                                "col_idx": col_idx
                            }
                        }
                    })

        return units

    # ---------------------------------------------------------
    # Document profile
    # ---------------------------------------------------------

    def _build_document_profile(
        self,
        parsed_doc: dict[str, Any],
        text_units: list[dict[str, Any]],
    ) -> dict[str, Any]:
        blocks = parsed_doc.get("blocks", [])
        tables = parsed_doc.get("tables", [])
        core_properties = parsed_doc.get("document", {}).get("core_properties", {})

        title = self._detect_title(blocks, text_units, core_properties)

        heading_blocks = [
            b for b in blocks
            if b.get("block_type") == "heading" and b.get("text_normalized")
        ]
        section_titles = [b["text_normalized"] for b in heading_blocks]
        top_headings = section_titles[:5]

        texts_for_keywords = [u["text"] for u in text_units if u.get("text")]
        keywords = extract_keywords_from_texts(texts_for_keywords, top_k=20)

        table_headers = []
        for table in tables:
            schema = table.get("schema_signature", {})
            header = schema.get("header") or []
            header = [compact_text(h) for h in header]
            if any(header):
                table_headers.append(header)

        first_meaningful_texts = [
            compact_text(u["text"])
            for u in text_units[:10]
            if compact_text(u.get("text", ""))
        ]

        return {
            "title": title,
            "top_headings": top_headings,
            "section_titles": section_titles,
            "keywords": keywords,
            "table_headers": table_headers,
            "first_meaningful_texts": first_meaningful_texts[:5],
        }

    def _detect_title(
        self,
        blocks: list[dict[str, Any]],
        text_units: list[dict[str, Any]],
        core_properties: dict[str, Any],
    ) -> str | None:
        core_title = compact_text(core_properties.get("title") or "")
        if core_title:
            return core_title

        # 1. Явный heading
        for block in blocks:
            if block.get("block_type") == "heading":
                text = compact_text(block.get("text_normalized") or "")
                if len(text) >= 5:
                    return text

        # 2. Первый содержательный text unit
        for unit in text_units:
            text = compact_text(unit.get("text") or "")
            if len(text) >= 5:
                return text

        return None

    # ---------------------------------------------------------
    # Style profile
    # ---------------------------------------------------------

    def _build_style_profile(self, text_units: list[dict[str, Any]]) -> dict[str, Any]:
        font_names = []
        font_sizes = []
        line_spacings = []
        first_line_indents = []
        alignments = []
        style_names = []

        for unit in text_units:
            style = unit.get("style") or {}
            pf = unit.get("paragraph_format") or {}
            runs = unit.get("runs") or []

            if style.get("name"):
                style_names.append(style["name"])

            if pf.get("alignment"):
                alignments.append(pf["alignment"])

            if pf.get("line_spacing") is not None:
                line_spacings.append(round_if_float(pf["line_spacing"], 2))

            if pf.get("first_line_indent_pt") is not None:
                first_line_indents.append(round_if_float(pf["first_line_indent_pt"], 1))

            for run in runs:
                if run.get("font_name"):
                    font_names.append(run["font_name"])
                if run.get("font_size_pt") is not None:
                    font_sizes.append(round_if_float(run["font_size_pt"], 1))

        return {
            "dominant_style_name": most_common_non_null(style_names),
            "dominant_font": most_common_non_null(font_names),
            "dominant_font_size_pt": most_common_non_null(font_sizes),
            "dominant_line_spacing": most_common_non_null(line_spacings),
            "dominant_first_line_indent_pt": most_common_non_null(first_line_indents),
            "dominant_alignment": most_common_non_null(alignments),
            "font_distribution": dict(Counter(font_names).most_common(10)),
            "font_size_distribution": dict(Counter(font_sizes).most_common(10)),
            "alignment_distribution": dict(Counter(alignments).most_common(10)),
            "style_name_distribution": dict(Counter(style_names).most_common(10)),
        }

    # ---------------------------------------------------------
    # Field candidates
    # ---------------------------------------------------------

    def _extract_field_candidates(
        self,
        text_units: list[dict[str, Any]],
        parsed_doc: dict[str, Any],
    ) -> list[dict[str, Any]]:
        candidates = []

        # 1. Поля по text units
        for unit in text_units:
            text = compact_text(unit.get("text", ""))
            if not text:
                continue

            matched = False
            for pattern in FIELD_PATTERNS:
                m = pattern.match(text)
                if not m:
                    continue

                field_name = compact_text(m.group(1))
                field_value = compact_text(m.group(2))

                candidates.append({
                    "block_id": unit.get("block_id"),
                    "table_id": unit.get("table_id"),
                    "row_idx": unit.get("row_idx"),
                    "col_idx": unit.get("col_idx"),
                    "field_name": field_name,
                    "field_value": field_value,
                    "field_value_normalized": field_value,
                    "is_empty_like": is_empty_like(field_value),
                    "source": unit.get("source"),
                    "anchor": unit.get("anchor"),
                })
                matched = True
                break

            if matched:
                continue

        # 2. Placeholder-based кандидаты из blocks верхнего уровня
        for block in parsed_doc.get("blocks", []):
            placeholders = block.get("placeholders") or []
            text = block.get("text_raw") or ""
            text_norm = block.get("text_normalized") or ""

            if placeholders:
                candidates.append({
                    "block_id": block.get("block_id"),
                    "table_id": None,
                    "row_idx": None,
                    "col_idx": None,
                    "field_name": None,
                    "field_value": text,
                    "field_value_normalized": text_norm,
                    "is_empty_like": True,
                    "source": "placeholder_detected_in_block",
                    "anchor": {
                        "block_id": block.get("block_id")
                    },
                })

        # 3. Placeholder-like тексты внутри table cells
        for unit in text_units:
            text = compact_text(unit.get("text", ""))
            if text and is_empty_like(text):
                candidates.append({
                    "block_id": unit.get("block_id"),
                    "table_id": unit.get("table_id"),
                    "row_idx": unit.get("row_idx"),
                    "col_idx": unit.get("col_idx"),
                    "field_name": None,
                    "field_value": text,
                    "field_value_normalized": text,
                    "is_empty_like": True,
                    "source": "placeholder_like_text_unit",
                    "anchor": unit.get("anchor"),
                })

        return candidates

    # ---------------------------------------------------------
    # Table signatures
    # ---------------------------------------------------------

    def _build_table_signatures(self, tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
        signatures = []

        for table in tables:
            schema = table.get("schema_signature") or {}
            header = [compact_text(h) for h in (schema.get("header") or [])]

            non_empty_header_cells = [h for h in header if h]
            header_kind = self._classify_table_header(non_empty_header_cells)

            signatures.append({
                "table_id": table.get("table_id"),
                "block_id": table.get("block_id"),
                "rows_count": schema.get("rows_count"),
                "cols_count": schema.get("cols_count"),
                "header": header,
                "table_style": (table.get("table_format") or {}).get("style"),
                "header_kind": header_kind,
            })

        return signatures

    def _classify_table_header(self, header_cells: list[str]) -> str:
        if not header_cells:
            return "empty"

        joined = " ".join(header_cells).lower()

        # Грубая эвристика:
        # если header огромный и похож на реквизиты/адрес/контакты — это не data header
        contact_markers = ["tel", "тел", "e-mail", "email", "www", "ул.", "street", "russia"]
        if len(joined) > 80 and any(marker in joined for marker in contact_markers):
            return "letterhead_like"

        if len(header_cells) >= 2 and all(len(x) < 40 for x in header_cells if x):
            return "data_header"

        return "generic"

    # ---------------------------------------------------------
    # Layout type
    # ---------------------------------------------------------

    def _detect_document_layout_type(
        self,
        parsed_doc: dict[str, Any],
        text_units: list[dict[str, Any]],
    ) -> str:
        blocks = parsed_doc.get("blocks", [])
        tables = parsed_doc.get("tables", [])

        block_paragraphs = sum(
            1 for b in blocks if b.get("block_type") in {"paragraph", "heading"}
        )
        table_blocks = sum(
            1 for b in blocks if b.get("block_type") == "table"
        )
        table_text_units = sum(
            1 for u in text_units if u.get("source") == "table_cell_paragraph"
        )

        if table_blocks > 0 and block_paragraphs == 0:
            # возможный бланк / табличная форма
            signatures = self._build_table_signatures(tables)
            if any(sig.get("header_kind") == "letterhead_like" for sig in signatures):
                return "letterhead_like"
            return "table_form"

        if table_blocks > 0 and block_paragraphs > 0:
            return "mixed"

        return "plain_text"
    
# import json
# from document_enricher import DocumentEnricherV2

# with open("parsed_sample_expanded.json", "r", encoding="utf-8") as f:
#     parsed_doc = json.load(f)

# enricher = DocumentEnricherV2()
# enriched_doc = enricher.enrich(parsed_doc)

# with open("enriched_sample_v2.json", "w", encoding="utf-8") as f:
#     json.dump(enriched_doc, f, ensure_ascii=False, indent=2)