"""
Tests unitaires pour le module Livreur
"""
import pytest
from fastapi import status


class TestLivreurAPI:
    """Tests pour les endpoints de l'API Livreur"""
    
    def test_create_livreur_success(self, client, sample_livreur_data):
        """Test de création d'un livreur avec succès"""
        response = client.post("/livreurs/", json=sample_livreur_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == sample_livreur_data["nom"]
        assert data["prenom"] == sample_livreur_data["prenom"]
        assert data["telephone"] == sample_livreur_data["telephone"]
        assert data["vehicule"] == sample_livreur_data["vehicule"]
        assert "id" in data
    
    def test_get_all_livreurs_empty(self, client):
        """Test de récupération de tous les livreurs quand la liste est vide"""
        response = client.get("/livreurs/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_all_livreurs_with_data(self, client, sample_livreur_data):
        """Test de récupération de tous les livreurs"""
        # Créer plusieurs livreurs
        for i in range(3):
            livreur_data = sample_livreur_data.copy()
            livreur_data["nom"] = f"Livreur{i}"
            client.post("/livreurs/", json=livreur_data)
        
        response = client.get("/livreurs/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_get_livreur_by_id_success(self, client, sample_livreur_data):
        """Test de récupération d'un livreur par son ID"""
        # Créer un livreur
        create_response = client.post("/livreurs/", json=sample_livreur_data)
        livreur_id = create_response.json()["id"]
        
        # Récupérer le livreur
        response = client.get(f"/livreurs/{livreur_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == livreur_id
        assert data["nom"] == sample_livreur_data["nom"]
    
    def test_get_livreur_by_id_not_found(self, client):
        """Test de récupération d'un livreur inexistant"""
        response = client.get("/livreurs/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_livreur_success(self, client, sample_livreur_data):
        """Test de mise à jour d'un livreur"""
        # Créer un livreur
        create_response = client.post("/livreurs/", json=sample_livreur_data)
        livreur_id = create_response.json()["id"]
        
        # Mettre à jour le livreur
        update_data = {
            "nom": "Nouveau Nom",
            "vehicule": "Moto",
            "zone_assignee": "Zone Nord"
        }
        response = client.put(f"/livreurs/{livreur_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == update_data["nom"]
        assert data["vehicule"] == update_data["vehicule"]
        assert data["zone_assignee"] == update_data["zone_assignee"]
    
    def test_update_livreur_not_found(self, client):
        """Test de mise à jour d'un livreur inexistant"""
        update_data = {"nom": "Nouveau Nom"}
        response = client.put("/livreurs/9999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_livreur_success(self, client, sample_livreur_data):
        """Test de suppression d'un livreur"""
        # Créer un livreur
        create_response = client.post("/livreurs/", json=sample_livreur_data)
        livreur_id = create_response.json()["id"]
        
        # Supprimer le livreur
        response = client.delete(f"/livreurs/{livreur_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Vérifier que le livreur n'existe plus
        get_response = client.get(f"/livreurs/{livreur_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_livreur_not_found(self, client):
        """Test de suppression d'un livreur inexistant"""
        response = client.delete("/livreurs/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

