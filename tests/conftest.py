"""
Configuration des fixtures pytest pour les tests unitaires
"""
import os
# Set testing environment variable before importing app
os.environ["TESTING"] = "1"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app


# Configuration de la base de données de test en mémoire
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_engine():
    """Crée un moteur de base de données de test pour chaque test"""
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Crée une session de base de données pour chaque test"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(test_db):
    """Crée un client de test FastAPI avec la base de données de test"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_client_data():
    """Données d'exemple pour un client expéditeur"""
    return {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@example.com",
        "telephone": "+33123456789",
        "adresse": "123 Rue de la Paix, Paris"
    }


@pytest.fixture
def sample_destinataire_data():
    """Données d'exemple pour un destinataire"""
    return {
        "nom": "Martin",
        "prenom": "Marie",
        "email": "marie.martin@example.com",
        "telephone": "+33987654321",
        "adresse": "456 Avenue des Champs, Lyon"
    }


@pytest.fixture
def sample_livreur_data():
    """Données d'exemple pour un livreur"""
    return {
        "nom": "Durand",
        "prenom": "Pierre",
        "telephone": "+33555666777",
        "vehicule": "Camionnette",
        "zone_assignee": "Zone Nord"
    }


@pytest.fixture
def sample_colis_data():
    """Données d'exemple pour un colis"""
    return {
        "description": "Colis fragile",
        "poids": "5kg",
        "statut": "créé",
        "ville_destination": "Lyon",
        "id_livreur": None,
        "id_client_expediteur": 1,
        "id_destinataire": 1,
        "id_zone": None
    }


@pytest.fixture
def sample_zone_data():
    """Données d'exemple pour une zone"""
    return {
        "nom": "Zone Nord",
        "description": "Zone de livraison Nord de Paris"
    }
