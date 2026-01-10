from pydantic import BaseModel, ConfigDict
from typing import Optional


class AssignmentCreate(BaseModel):
    colis_id: int
    livreur_id: int
    zone_id: Optional[int] = None


class AssignmentResponse(BaseModel):
    colis_id: int
    livreur_id: int
    zone_id: Optional[int]
    message: str

    model_config = ConfigDict(from_attributes=True)
