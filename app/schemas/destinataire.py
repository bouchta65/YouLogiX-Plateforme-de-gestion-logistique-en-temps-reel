from pydantic import BaseModel, EmailStr

class DestinataireBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    adresse: str  

class DestinataireCreate(DestinataireBase):
    pass


class DestinataireUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    email: EmailStr | None = None
    telephone: str | None = None
    adresse: str | None = None
    
class DestinataireRead(DestinataireBase):
    id: int
    class Config:
        orm_mode = True 
