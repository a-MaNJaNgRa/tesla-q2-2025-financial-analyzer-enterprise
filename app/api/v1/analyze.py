mkdir -p app/api/v1
cat > app/api/v1/analyze.py << 'EOF'
from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException, Security
from app.core.security import verify_api_key
from app.core.middleware import limiter
from app.services.analyzer_service import analyze_pdf
from app.utils.pdf_validator import is_valid_pdf
import os
import uuid

router = APIRouter()

@router.post("/analyze")
@limiter.limit("100/hour")
async def analyze(
    file: UploadFile = File(...),
    query: str = Form(...),
    _: str = Security(verify_api_key)
):
    content_preview = await file.read(1024)
    if not file.filename.lower().endswith('.pdf') or not is_valid_pdf(content_preview):
        raise HTTPException(status_code=400, detail="Invalid PDF file")

    await file.seek(0)
    content = await file.read()
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 15MB)")

    file_path = f"/tmp/{uuid.uuid4()}.pdf"
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        result = await analyze_pdf(file_path, query)
        return {
            "status": "success",
            "query": query,
            "analysis": result,
            "file_processed": file.filename
        }
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
EOF
