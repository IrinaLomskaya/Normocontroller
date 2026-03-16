from typing import Any

from app.workers.parser import DocxNormalizer
from app.workers.document_enricher import DocumentEnricherV2
from app.workers.template_profile_builder import TemplateProfileBuilder
from app.workers.template_selector import TemplateSelector


class DocumentPipeline:
    def __init__(self) -> None:
        self.parser = DocxNormalizer()
        self.enricher = DocumentEnricherV2()
        self.profile_builder = TemplateProfileBuilder()
        self.selector = TemplateSelector()

    def build_profile(self, file_path: str, doc_role: str) -> dict[str, Any]:
        parsed = self.parser.parse(file_path)
        enriched = self.enricher.enrich(parsed)
        profile = self.profile_builder.build(enriched, doc_role=doc_role)
        return profile

    def debug_full(self, file_path: str, doc_role: str) -> dict[str, Any]:
        parsed = self.parser.parse(file_path)
        enriched = self.enricher.enrich(parsed)
        profile = self.profile_builder.build(enriched, doc_role=doc_role)

        return {
            "parsed": parsed,
            "enriched": enriched,
            "profile": profile,
        }

    def select_template(
        self,
        user_file_path: str,
        template_profiles: list[dict[str, Any]],
    ) -> dict[str, Any]:
        user_profile = self.build_profile(user_file_path, doc_role="user")
        return self.selector.select(user_profile, template_profiles, top_k=3)