import os
import uuid
from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException, Security

from app.core.security import verify_api_key
from app.core.database import get_db
from app.services.analyzer_service import analyze_pdf
from app.schemas.analysis import AnalysisResponse
from app.utils.pdf_validator import is_valid_pdf
from app.core.config import get_settings

settings = get_settings()

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    file: UploadFile = File(...),
    query: str = Form(...),
    db=Depends(get_db),
    _: str = Security(verify_api_key),
):
    # Validate extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Read first 1024 bytes for signature validation
    first_bytes = await file.read(1024)
    if not is_valid_pdf(first_bytes):
        raise HTTPException(status_code=400, detail="Invalid PDF file")

    # Reset pointer
    await file.seek(0)

    content = await file.read()

    # Size validation
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    # Save temp file
    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_path = os.path.join("temp_" + temp_filename)

    with open(temp_path, "wb") as f:
        f.write(content)

    try:
        result = await analyze_pdf(temp_path, query)

        return AnalysisResponse(
            status="success",
            analysis=result,
        )

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)