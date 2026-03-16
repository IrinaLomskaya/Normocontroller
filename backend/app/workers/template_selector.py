from __future__ import annotations

from typing import Any


def jaccard_similarity(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def normalize_text_for_match(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.lower().strip().split())


def safe_set(items: list[str] | None) -> set[str]:
    if not items:
        return set()
    return {normalize_text_for_match(x) for x in items if normalize_text_for_match(x)}


def title_similarity(user_title: str | None, ref_title: str | None) -> float:
    u = normalize_text_for_match(user_title)
    r = normalize_text_for_match(ref_title)

    if not u and not r:
        return 1.0
    if not u or not r:
        return 0.0
    if u == r:
        return 1.0

    return jaccard_similarity(set(u.split()), set(r.split()))


def keyword_similarity(user_keywords: list[str], ref_keywords: list[str]) -> float:
    return jaccard_similarity(safe_set(user_keywords), safe_set(ref_keywords))


def section_similarity(user_sections: list[str], ref_sections: list[str]) -> float:
    return jaccard_similarity(safe_set(user_sections), safe_set(ref_sections))


def layout_similarity(user_layout: str | None, ref_layout: str | None) -> float:
    if not user_layout and not ref_layout:
        return 1.0
    if not user_layout or not ref_layout:
        return 0.0
    return 1.0 if user_layout == ref_layout else 0.0


def style_similarity(user_style: dict[str, Any], ref_style: dict[str, Any]) -> float:
    score = 0.0
    parts = 0

    uf = normalize_text_for_match(user_style.get("dominant_font"))
    rf = normalize_text_for_match(ref_style.get("dominant_font"))
    parts += 1
    if uf and rf and uf == rf:
        score += 1.0

    ufs = user_style.get("dominant_font_size_pt")
    rfs = ref_style.get("dominant_font_size_pt")
    parts += 1
    if ufs is not None and rfs is not None and abs(float(ufs) - float(rfs)) <= 0.5:
        score += 1.0

    ua = normalize_text_for_match(user_style.get("dominant_alignment"))
    ra = normalize_text_for_match(ref_style.get("dominant_alignment"))
    parts += 1
    if ua and ra and ua == ra:
        score += 1.0

    return score / parts if parts else 0.0


def extract_table_headers(profile: dict[str, Any]) -> set[str]:
    headers = set()
    for table in profile.get("table_signatures", []):
        for cell in table.get("header", []):
            cell_norm = normalize_text_for_match(cell)
            if cell_norm:
                headers.add(cell_norm)
    return headers


def table_similarity(user_profile: dict[str, Any], ref_profile: dict[str, Any]) -> float:
    user_headers = extract_table_headers(user_profile)
    ref_headers = extract_table_headers(ref_profile)

    header_score = jaccard_similarity(user_headers, ref_headers)

    user_table_count = len(user_profile.get("table_signatures", []))
    ref_table_count = len(ref_profile.get("table_signatures", []))

    if user_table_count == 0 and ref_table_count == 0:
        count_score = 1.0
    elif user_table_count == 0 or ref_table_count == 0:
        count_score = 0.0
    else:
        count_score = 1.0 - min(
            abs(user_table_count - ref_table_count) / max(user_table_count, ref_table_count),
            1.0,
        )

    return 0.7 * header_score + 0.3 * count_score


class TemplateSelector:
    def __init__(self) -> None:
        self.weights = {
            "title": 0.10,
            "keywords": 0.10,
            "sections": 0.20,
            "tables": 0.30,
            "layout": 0.20,
            "style": 0.10,
        }

    def select(
        self,
        user_profile: dict[str, Any],
        reference_profiles: list[dict[str, Any]],
        top_k: int = 3,
    ) -> dict[str, Any]:
        filtered_refs = self._prefilter(user_profile, reference_profiles)

        scored = []
        for ref in filtered_refs:
            scored.append(self._score_pair(user_profile, ref))

        scored.sort(key=lambda x: x["final_score"], reverse=True)
        best = scored[0] if scored else None

        return {
            "selected_template_id": best["normative_id"] if best else None,
            "selected_title": best["title"] if best else None,
            "confidence": round(best["final_score"], 4) if best else 0.0,
            "top_candidates": scored[:top_k],
        }

    def _prefilter(
        self,
        user_profile: dict[str, Any],
        reference_profiles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        user_layout = user_profile.get("document_layout_type")
        user_table_count = len(user_profile.get("table_signatures", []))

        result = []
        for ref in reference_profiles:
            ref_layout = ref.get("document_layout_type")
            ref_table_count = len(ref.get("table_signatures", []))

            # мягкий фильтр по layout
            if user_layout == "plain_text" and ref_layout in {"table_form", "letterhead_like"} and user_table_count == 0:
                continue

            if user_layout in {"table_form", "letterhead_like"} and ref_table_count == 0:
                continue

            result.append(ref)

        return result if result else reference_profiles

    def _score_pair(
        self,
        user_profile: dict[str, Any],
        ref_profile: dict[str, Any],
    ) -> dict[str, Any]:
        title_score = title_similarity(user_profile.get("title"), ref_profile.get("title"))
        keyword_score = keyword_similarity(user_profile.get("keywords", []), ref_profile.get("keywords", []))
        section_score = section_similarity(user_profile.get("section_titles", []), ref_profile.get("section_titles", []))
        table_score = table_similarity(user_profile, ref_profile)
        layout_score = layout_similarity(user_profile.get("document_layout_type"), ref_profile.get("document_layout_type"))
        style_score = style_similarity(user_profile.get("style_profile", {}), ref_profile.get("style_profile", {}))

        final_score = (
            self.weights["title"] * title_score +
            self.weights["keywords"] * keyword_score +
            self.weights["sections"] * section_score +
            self.weights["tables"] * table_score +
            self.weights["layout"] * layout_score +
            self.weights["style"] * style_score
        )

        return {
            "normative_id": ref_profile.get("normative_id"),
            "title": ref_profile.get("title"),
            "filename": ref_profile.get("filename"),
            "doc_role": ref_profile.get("doc_role"),
            "document_layout_type": ref_profile.get("document_layout_type"),
            "final_score": round(final_score, 4),
            "score_breakdown": {
                "title_score": round(title_score, 4),
                "keyword_score": round(keyword_score, 4),
                "section_score": round(section_score, 4),
                "table_score": round(table_score, 4),
                "layout_score": round(layout_score, 4),
                "style_score": round(style_score, 4),
            },
        }
    
# import json
# from template_selector import TemplateSelector

# with open("user_template_profile.json", "r", encoding="utf-8") as f:
#     user_profile = json.load(f)

# with open("template_profiles.json", "r", encoding="utf-8") as f:
#     template_profiles = json.load(f)

# selector = TemplateSelector()
# result = selector.select(user_profile, template_profiles, top_k=3)

# print(json.dumps(result, ensure_ascii=False, indent=2))