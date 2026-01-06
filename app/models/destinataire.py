from sqlalchemy import Column, Integer, String
from core.config import Base

class Destinataire(Base):
    __tablename__ = "destinataires"

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telephone = Column(String, nullable=False)
    adresse = Column(String, nullable=False)
