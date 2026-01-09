from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    code_postal = Column(String, nullable=False)
