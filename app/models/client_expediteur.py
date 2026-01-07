from sqlalchemy import Column, Integer, String
from app.core.database import Base

class ClientExpediteur(Base):
    __tablename__ = "client_expediteur"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    email = Column(String, unique=True)
    telephone = Column(String)
    adresse = Column(String)

