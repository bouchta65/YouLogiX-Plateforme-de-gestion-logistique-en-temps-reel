"""
Tests unitaires pour le module Zone
"""
import pytest
from fastapi import status


class TestZoneAPI:
    """Tests pour les endpoints de l'API Zone"""
    
    def test_create_zone_success(self, client, sample_zone_data):
        """Test de création d'une zone avec succès"""
        response = client.post("/zones/", json=sample_zone_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == sample_zone_data["nom"]
        assert data["description"] == sample_zone_data["description"]
        assert "id" in data
    
    def test_get_all_zones_empty(self, client):
        """Test de récupération de toutes les zones quand la liste est vide"""
        response = client.get("/zones/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_all_zones_with_data(self, client, sample_zone_data):
        """Test de récupération de toutes les zones"""
        # Créer plusieurs zones
        for i in range(3):
            zone_data = sample_zone_data.copy()
            zone_data["nom"] = f"Zone {i}"
            client.post("/zones/", json=zone_data)
        
        response = client.get("/zones/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_get_zone_by_id_success(self, client, sample_zone_data):
        """Test de récupération d'une zone par son ID"""
        # Créer une zone
        create_response = client.post("/zones/", json=sample_zone_data)
        zone_id = create_response.json()["id"]
        
        # Récupérer la zone
        response = client.get(f"/zones/{zone_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == zone_id
        assert data["nom"] == sample_zone_data["nom"]
        assert data["description"] == sample_zone_data["description"]
    
    def test_get_zone_by_id_not_found(self, client):
        """Test de récupération d'une zone inexistante"""
        response = client.get("/zones/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Zone not found"
    
    def test_create_zone_without_description(self, client):
        """Test de création d'une zone sans description (optionnelle)"""
        zone_data = {"nom": "Zone Test"}
        response = client.post("/zones/", json=zone_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == "Zone Test"
        assert data["description"] is None

