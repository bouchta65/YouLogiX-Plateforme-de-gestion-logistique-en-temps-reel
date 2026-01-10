"""
Tests unitaires pour le module Destinataire
"""
import pytest
from fastapi import status


class TestDestinataireAPI:
    """Tests pour les endpoints de l'API Destinataire"""
    
    def test_create_destinataire_success(self, client, sample_destinataire_data):
        """Test de création d'un destinataire avec succès"""
        response = client.post("/destinataires/", json=sample_destinataire_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == sample_destinataire_data["nom"]
        assert data["prenom"] == sample_destinataire_data["prenom"]
        assert data["email"] == sample_destinataire_data["email"]
        assert data["telephone"] == sample_destinataire_data["telephone"]
        assert data["adresse"] == sample_destinataire_data["adresse"]
        assert "id" in data
    
    def test_get_all_destinataires_empty(self, client):
        """Test de récupération de tous les destinataires quand la liste est vide"""
        response = client.get("/destinataires/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_all_destinataires_with_data(self, client, sample_destinataire_data):
        """Test de récupération de tous les destinataires"""
        # Créer plusieurs destinataires
        for i in range(3):
            dest_data = sample_destinataire_data.copy()
            dest_data["email"] = f"destinataire{i}@example.com"
            client.post("/destinataires/", json=dest_data)
        
        response = client.get("/destinataires/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_get_destinataire_by_id_success(self, client, sample_destinataire_data):
        """Test de récupération d'un destinataire par son ID"""
        # Créer un destinataire
        create_response = client.post("/destinataires/", json=sample_destinataire_data)
        destinataire_id = create_response.json()["id"]
        
        # Récupérer le destinataire
        response = client.get(f"/destinataires/{destinataire_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == destinataire_id
        assert data["nom"] == sample_destinataire_data["nom"]
    
    def test_get_destinataire_by_id_not_found(self, client):
        """Test de récupération d'un destinataire inexistant"""
        response = client.get("/destinataires/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_destinataire_success(self, client, sample_destinataire_data):
        """Test de mise à jour d'un destinataire"""
        # Créer un destinataire
        create_response = client.post("/destinataires/", json=sample_destinataire_data)
        destinataire_id = create_response.json()["id"]
        
        # Mettre à jour le destinataire
        update_data = {
            "nom": "Nouveau Nom",
            "telephone": "+33111222333"
        }
        response = client.put(f"/destinataires/{destinataire_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == update_data["nom"]
        assert data["telephone"] == update_data["telephone"]
    
    def test_update_destinataire_not_found(self, client):
        """Test de mise à jour d'un destinataire inexistant"""
        update_data = {"nom": "Nouveau Nom"}
        response = client.put("/destinataires/9999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_destinataire_success(self, client, sample_destinataire_data):
        """Test de suppression d'un destinataire"""
        # Créer un destinataire
        create_response = client.post("/destinataires/", json=sample_destinataire_data)
        destinataire_id = create_response.json()["id"]
        
        # Supprimer le destinataire
        response = client.delete(f"/destinataires/{destinataire_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Vérifier que le destinataire n'existe plus
        get_response = client.get(f"/destinataires/{destinataire_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_destinataire_not_found(self, client):
        """Test de suppression d'un destinataire inexistant"""
        response = client.delete("/destinataires/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

