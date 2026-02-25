from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    status: str
    analysis: str