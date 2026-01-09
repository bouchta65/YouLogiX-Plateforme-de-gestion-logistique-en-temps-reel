from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.core.database import Base

class HistoriqueStatut(Base):
    __tablename__ = "historique_statuts"

    id = Column(Integer, primary_key=True)
    id_colis = Column(Integer, ForeignKey("colis.id"), nullable=False)
    ancien_statut = Column(String, nullable=False)
    nouveau_statut = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    id_livreur = Column(Integer, ForeignKey("livreurs.id"), nullable=True)
