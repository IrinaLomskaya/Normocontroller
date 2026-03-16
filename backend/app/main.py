from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List, Annotated

from app.schemas import TemplateSelectionResponse, TemplateProfileResponse, ParseDebugResponse
from app.storage.in_memory_repo import InMemoryTemplateRepository
from app.services.pipeline import DocumentPipeline

app = FastAPI(title="NormControl API", version="0.1.0")

pipeline = DocumentPipeline()
template_repo = InMemoryTemplateRepository()


def save_upload_to_temp(upload: UploadFile) -> str:
    suffix = Path(upload.filename).suffix or ".docx"
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = upload.file.read()
        tmp.write(content)
        return tmp.name


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/templates/upload", response_model=TemplateProfileResponse)
def upload_template(file: UploadFile = File(...)) -> dict:
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail=f"Only .docx supported: {file.filename}")

    tmp_path = save_upload_to_temp(file)
    profile = pipeline.build_profile(tmp_path, doc_role="template")
    template_repo.add(profile)

    return {
        "template_id": profile["template_id"],
        "title": profile.get("title"),
        "filename": profile.get("filename"),
        "document_layout_type": profile.get("document_layout_type"),
        "keywords": profile.get("keywords", []),
        "stats": profile.get("stats", {}),
    }

@app.post("/templates/upload-batch", response_model=list[TemplateProfileResponse])
def upload_templates_batch(
    files: Annotated[list[UploadFile], File(...)]
) -> list[dict]:
    created = []

    for file in files:
        if not file.filename.endswith(".docx"):
            raise HTTPException(status_code=400, detail=f"Only .docx supported: {file.filename}")

        tmp_path = save_upload_to_temp(file)
        profile = pipeline.build_profile(tmp_path, doc_role="template")
        template_repo.add(profile)

        created.append({
            "template_id": profile["template_id"],
            "title": profile.get("title"),
            "filename": profile.get("filename"),
            "document_layout_type": profile.get("document_layout_type"),
            "keywords": profile.get("keywords", []),
            "stats": profile.get("stats", {}),
        })

    return created



@app.get("/templates")
def list_templates() -> list[dict]:
    return template_repo.list_all()


@app.delete("/templates")
def clear_templates() -> dict:
    template_repo.clear()
    return {"status": "cleared"}


@app.post("/documents/check", response_model=TemplateSelectionResponse)
def check_document(file: UploadFile = File(...)) -> dict:
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx supported")

    template_profiles = template_repo.list_all()
    if not template_profiles:
        raise HTTPException(status_code=400, detail="No templates uploaded")

    tmp_path = save_upload_to_temp(file)
    result = pipeline.select_template(tmp_path, template_profiles)
    return result


@app.post("/debug/profile", response_model=ParseDebugResponse)
def debug_profile(
    file: UploadFile = File(...),
    doc_role: str = "user",
) -> dict:
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx supported")

    tmp_path = save_upload_to_temp(file)
    result = pipeline.debug_full(tmp_path, doc_role=doc_role)
    return result