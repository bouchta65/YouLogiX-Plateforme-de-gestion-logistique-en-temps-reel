from pydantic import BaseModel
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

    class Config:
        from_attributes = True
