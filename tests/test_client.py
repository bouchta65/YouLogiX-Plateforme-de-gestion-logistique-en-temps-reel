"""
Tests unitaires pour le module Client Expéditeur
"""
import pytest
from fastapi import status


class TestClientAPI:
    
    def test_create_client_success(self, client, sample_client_data):

        response = client.post("/clients/", json=sample_client_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == sample_client_data["nom"]
        assert data["prenom"] == sample_client_data["prenom"]
        assert data["email"] == sample_client_data["email"]
        assert data["telephone"] == sample_client_data["telephone"]
        assert data["adresse"] == sample_client_data["adresse"]
        assert "id" in data
    
    def test_create_client_duplicate_email(self, client, sample_client_data):

        client.post("/clients/", json=sample_client_data)
        
        response = client.post("/clients/", json=sample_client_data)
        
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "existe déjà" in response.json()["detail"]
    
    def test_get_all_clients_empty(self, client):
        response = client.get("/clients/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_all_clients_with_data(self, client, sample_client_data):

        for i in range(3):
            client_data = sample_client_data.copy()
            client_data["email"] = f"client{i}@example.com"
            client.post("/clients/", json=client_data)
        
        response = client.get("/clients/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_get_client_by_id_success(self, client, sample_client_data):


        create_response = client.post("/clients/", json=sample_client_data)
        client_id = create_response.json()["id"]
        
        response = client.get(f"/clients/{client_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == client_id
        assert data["nom"] == sample_client_data["nom"]
    
    def test_get_client_by_id_not_found(self, client):

        response = client.get("/clients/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_client_success(self, client, sample_client_data):


        create_response = client.post("/clients/", json=sample_client_data)
        client_id = create_response.json()["id"]
        
        update_data = {
            "nom": "Nouveau Nom",
            "prenom": "Nouveau Prenom",
            "telephone": "+33111222333"
        }
        response = client.put(f"/clients/{client_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == update_data["nom"]
        assert data["prenom"] == update_data["prenom"]
        assert data["telephone"] == update_data["telephone"]
        assert data["email"] == sample_client_data["email"]
    
    def test_update_client_not_found(self, client):

        update_data = {"nom": "Nouveau Nom"}
        response = client.put("/clients/9999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_client_success(self, client, sample_client_data):

        create_response = client.post("/clients/", json=sample_client_data)
        client_id = create_response.json()["id"]
        
        response = client.delete(f"/clients/{client_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        

        get_response = client.get(f"/clients/{client_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_client_not_found(self, client):

        response = client.delete("/clients/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

