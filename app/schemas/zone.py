from pydantic import BaseModel, ConfigDict
from typing import Optional


class ZoneBase(BaseModel):
    nom: str
    description: Optional[str] = None


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None


class ZoneRead(ZoneBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
