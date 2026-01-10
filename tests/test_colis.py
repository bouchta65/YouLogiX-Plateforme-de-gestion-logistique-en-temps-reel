import pytest
from fastapi import status
from app.models.client_expediteur import ClientExpediteur
from app.models.destinataire import Destinataire
from app.models.colis import Colis, StatutColis


class TestColisAPI:
    
    def test_create_colis_success(self, client, test_db, sample_colis_data, 
                                   sample_client_data, sample_destinataire_data):
        
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        test_db.refresh(db_client)
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        test_db.refresh(db_dest)
        

        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        
        response = client.post("/colis/", json=sample_colis_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["description"] == sample_colis_data["description"]
        assert data["poids"] == sample_colis_data["poids"]
        assert data["statut"] == sample_colis_data["statut"]
        assert data["ville_destination"] == sample_colis_data["ville_destination"]
        assert "id" in data
    
    def test_get_all_colis_empty(self, client):

        response = client.get("/colis/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_all_colis_with_data(self, client, test_db, sample_colis_data,
                                     sample_client_data, sample_destinataire_data):
        
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        

        for i in range(3):
            colis_data = sample_colis_data.copy()
            colis_data["description"] = f"Colis {i}"
            colis_data["id_client_expediteur"] = db_client.id
            colis_data["id_destinataire"] = db_dest.id
            client.post("/colis/", json=colis_data)
        
        response = client.get("/colis/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_get_colis_by_id_success(self, client, test_db, sample_colis_data,
                                     sample_client_data, sample_destinataire_data):
        
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        
        create_response = client.post("/colis/", json=sample_colis_data)
        colis_id = create_response.json()["id"]
        
        response = client.get(f"/colis/{colis_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == colis_id
        assert data["description"] == sample_colis_data["description"]
    
    def test_get_colis_by_id_not_found(self, client):

        response = client.get("/colis/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Colis not found"
    
    def test_update_colis_success(self, client, test_db, sample_colis_data,
                                  sample_client_data, sample_destinataire_data):
        
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        
        create_response = client.post("/colis/", json=sample_colis_data)
        colis_id = create_response.json()["id"]
        
        update_data = {
            "description": "Colis mis à jour",
            "statut": "en transit",
            "poids": "7kg"
        }
        response = client.put(f"/colis/{colis_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["description"] == update_data["description"]
        assert data["statut"] == update_data["statut"]
        assert data["poids"] == update_data["poids"]
    
    def test_update_colis_not_found(self, client):

        update_data = {"description": "Nouveau texte"}
        response = client.put("/colis/9999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_colis_success(self, client, test_db, sample_colis_data,
                                  sample_client_data, sample_destinataire_data):
        
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        
        
        create_response = client.post("/colis/", json=sample_colis_data)
        colis_id = create_response.json()["id"]
        
       
        response = client.delete(f"/colis/{colis_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        
        get_response = client.get(f"/colis/{colis_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_colis_not_found(self, client):

        response = client.delete("/colis/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestColisController:
    
    def test_create_colis_in_db(self, test_db, sample_colis_data,
                                sample_client_data, sample_destinataire_data):
        
        from app.controllers.colis_controller import create_colis
        from app.schemas.colis import ColisCreate
        
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        
        colis_create = ColisCreate(**sample_colis_data)
        db_colis = create_colis(test_db, colis_create)
        
        assert db_colis.id is not None
        assert db_colis.description == sample_colis_data["description"]
        assert db_colis.poids == sample_colis_data["poids"]
    
    def test_get_all_colis_from_db(self, test_db, sample_colis_data,
                                   sample_client_data, sample_destinataire_data):
        
        from app.controllers.colis_controller import create_colis, get_all_colis
        from app.schemas.colis import ColisCreate
        
        
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        

        for i in range(3):
            colis_data = sample_colis_data.copy()
            colis_data["description"] = f"Colis {i}"
            colis_create = ColisCreate(**colis_data)
            create_colis(test_db, colis_create)
        
        all_colis = get_all_colis(test_db)
        
        assert len(all_colis) == 3
    
    def test_update_colis_in_db(self, test_db, sample_colis_data,
                                sample_client_data, sample_destinataire_data):
        """Test de mise à jour d'un colis dans la base de données"""
        from app.controllers.colis_controller import create_colis, update_colis
        from app.schemas.colis import ColisCreate, ColisUpdate
        

        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        

        colis_create = ColisCreate(**sample_colis_data)
        db_colis = create_colis(test_db, colis_create)
        

        update_data = ColisUpdate(description="Nouvelle description", statut="livré")
        updated_colis = update_colis(test_db, db_colis.id, update_data)
        
        assert updated_colis.description == "Nouvelle description"
        assert updated_colis.statut.value == "livré"
    
    def test_delete_colis_from_db(self, test_db, sample_colis_data,
                                  sample_client_data, sample_destinataire_data):
        from app.controllers.colis_controller import create_colis, delete_colis, get_colis_by_id
        from app.schemas.colis import ColisCreate
        
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        
        colis_create = ColisCreate(**sample_colis_data)
        db_colis = create_colis(test_db, colis_create)
        colis_id = db_colis.id
        
        deleted_colis = delete_colis(test_db, colis_id)
        
        assert deleted_colis.id == colis_id
        
        assert get_colis_by_id(test_db, colis_id) is None

