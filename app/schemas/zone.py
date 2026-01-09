from pydantic import BaseModel
from typing import Optional


class ZoneBase(BaseModel):
    nom: str
    code_postal: str

class ZoneCreate(ZoneBase):
    pass

class ZoneUpdate(BaseModel):
    nom: Optional[str] = None
    code_postal: Optional[str] = None

class ZoneRead(ZoneBase):
    id: int

    class Config:
        from_attributes = True
