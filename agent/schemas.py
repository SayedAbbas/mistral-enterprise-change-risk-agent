from typing import Literal
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source: str
    evidence_id: str
    finding: str


class RiskAssessment(BaseModel):
    change_id: str
    risk: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    summary: str
    evidence: list[Evidence]
    mitigations: list[str]
    requires_human_approval: bool = True
    confidence: float = Field(ge=0, le=1)
