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
        
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT, status.HTTP_500_INTERNAL_SERVER_ERROR]
    
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


class TestClientController:

    
    def test_create_client_in_db(self, test_db, sample_client_data):

        from app.controllers.client_controller import create_client
        from app.schemas.client_expediteur import ClientExpediteurCreate
        
        client_create = ClientExpediteurCreate(**sample_client_data)
        db_client = create_client(test_db, client_create)
        
        assert db_client.id is not None
        assert db_client.nom == sample_client_data["nom"]
        assert db_client.prenom == sample_client_data["prenom"]
        assert db_client.email == sample_client_data["email"]
    
    def test_get_clients_from_db(self, test_db, sample_client_data):

        from app.controllers.client_controller import create_client, get_clients
        from app.schemas.client_expediteur import ClientExpediteurCreate
        
        for i in range(3):
            client_data = sample_client_data.copy()
            client_data["email"] = f"client{i}@example.com"
            client_create = ClientExpediteurCreate(**client_data)
            create_client(test_db, client_create)
        
        all_clients = get_clients(test_db)
        
        assert len(all_clients) == 3
    
    def test_get_client_by_id_from_db(self, test_db, sample_client_data):

        from app.controllers.client_controller import create_client, get_clients_by_id
        from app.schemas.client_expediteur import ClientExpediteurCreate
        
        client_create = ClientExpediteurCreate(**sample_client_data)
        db_client = create_client(test_db, client_create)
        
        retrieved_client = get_clients_by_id(test_db, db_client.id)
        
        assert retrieved_client is not None
        assert retrieved_client.id == db_client.id
        assert retrieved_client.email == sample_client_data["email"]
    
    def test_update_client_in_db(self, test_db, sample_client_data):

        from app.controllers.client_controller import create_client, update_client
        from app.schemas.client_expediteur import ClientExpediteurCreate, ClientExpediteurUpdate
        
     
        client_create = ClientExpediteurCreate(**sample_client_data)
        db_client = create_client(test_db, client_create)
        
      
        update_data = ClientExpediteurUpdate(nom="Nom Mis à Jour", telephone="+33999888777")
        updated_client = update_client(test_db, db_client.id, update_data)
        
        assert updated_client.nom == "Nom Mis à Jour"
        assert updated_client.telephone == "+33999888777"

        assert updated_client.email == sample_client_data["email"]
    
    def test_update_client_not_found_in_db(self, test_db):

        from app.controllers.client_controller import update_client
        from app.schemas.client_expediteur import ClientExpediteurUpdate
        
        update_data = ClientExpediteurUpdate(nom="Nom Test")
        result = update_client(test_db, 9999, update_data)
        
        assert result is None
    
    def test_delete_client_from_db(self, test_db, sample_client_data):

        from app.controllers.client_controller import create_client, delete_client, get_clients_by_id
        from app.schemas.client_expediteur import ClientExpediteurCreate
        
       
        client_create = ClientExpediteurCreate(**sample_client_data)
        db_client = create_client(test_db, client_create)
        client_id = db_client.id
        
       
        deleted_client = delete_client(test_db, client_id)
        
        assert deleted_client.id == client_id
        
        
        assert get_clients_by_id(test_db, client_id) is None
    
    def test_delete_client_not_found_in_db(self, test_db):
        """Test de suppression d'un client inexistant de la base de données"""
        from app.controllers.client_controller import delete_client
        
        result = delete_client(test_db, 9999)
        
        assert result is None

