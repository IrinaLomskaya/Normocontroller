from pydantic import BaseModel
from typing import Any, Optional


class TemplateProfileResponse(BaseModel):
    template_id: str
    title: Optional[str] = None
    filename: str
    document_layout_type: Optional[str] = None
    keywords: list[str]
    stats: dict[str, Any]


class TemplateSelectionResponse(BaseModel):
    selected_template_id: Optional[str]
    selected_title: Optional[str]
    confidence: float
    top_candidates: list[dict[str, Any]]


class ParseDebugResponse(BaseModel):
    parsed: dict[str, Any]
    enriched: dict[str, Any]
    profile: dict[str, Any]