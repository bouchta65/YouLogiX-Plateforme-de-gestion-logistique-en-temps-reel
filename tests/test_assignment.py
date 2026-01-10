"""
Tests unitaires pour le module Assignment (Assignation des colis aux livreurs)
"""
import pytest
from fastapi import status
from app.models.client_expediteur import ClientExpediteur
from app.models.destinataire import Destinataire
from app.models.livreur import Livreur
from app.models.zone import Zone


class TestAssignmentAPI:
    """Tests pour les endpoints de l'API Assignment"""
    
    def test_assign_colis_to_livreur_success(self, client, test_db, sample_colis_data,
                                             sample_client_data, sample_destinataire_data, 
                                             sample_livreur_data, sample_zone_data):
        """Test d'assignation d'un colis à un livreur avec succès"""
        # Créer les données nécessaires
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        db_livreur = Livreur(**sample_livreur_data)
        test_db.add(db_livreur)
        test_db.commit()
        
        db_zone = Zone(**sample_zone_data)
        test_db.add(db_zone)
        test_db.commit()
        
        # Créer un colis
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        colis_response = client.post("/colis/", json=sample_colis_data)
        colis_id = colis_response.json()["id"]
        
        # Assigner le colis au livreur
        assignment_data = {
            "colis_id": colis_id,
            "livreur_id": db_livreur.id,
            "zone_id": db_zone.id
        }
        response = client.post("/assignments/", json=assignment_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["colis_id"] == colis_id
        assert data["livreur_id"] == db_livreur.id
        assert data["zone_id"] == db_zone.id
        assert "message" in data
    
    def test_assign_colis_without_zone(self, client, test_db, sample_colis_data,
                                       sample_client_data, sample_destinataire_data, 
                                       sample_livreur_data):
        """Test d'assignation d'un colis à un livreur sans zone"""
        # Créer les données nécessaires
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        db_livreur = Livreur(**sample_livreur_data)
        test_db.add(db_livreur)
        test_db.commit()
        
        # Créer un colis
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        colis_response = client.post("/colis/", json=sample_colis_data)
        colis_id = colis_response.json()["id"]
        
        # Assigner le colis au livreur sans zone
        assignment_data = {
            "colis_id": colis_id,
            "livreur_id": db_livreur.id
        }
        response = client.post("/assignments/", json=assignment_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["colis_id"] == colis_id
        assert data["livreur_id"] == db_livreur.id
    
    def test_assign_colis_not_found(self, client, test_db, sample_livreur_data):
        """Test d'assignation d'un colis inexistant"""
        db_livreur = Livreur(**sample_livreur_data)
        test_db.add(db_livreur)
        test_db.commit()
        
        assignment_data = {
            "colis_id": 9999,
            "livreur_id": db_livreur.id
        }
        response = client.post("/assignments/", json=assignment_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_assign_livreur_not_found(self, client, test_db, sample_colis_data,
                                      sample_client_data, sample_destinataire_data):
        """Test d'assignation à un livreur inexistant"""
        # Créer les données nécessaires
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        # Créer un colis
        sample_colis_data["id_client_expediteur"] = db_client.id
        sample_colis_data["id_destinataire"] = db_dest.id
        colis_response = client.post("/colis/", json=sample_colis_data)
        colis_id = colis_response.json()["id"]
        
        assignment_data = {
            "colis_id": colis_id,
            "livreur_id": 9999
        }
        response = client.post("/assignments/", json=assignment_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_assigned_colis(self, client, test_db, sample_colis_data,
                                sample_client_data, sample_destinataire_data, 
                                sample_livreur_data):
        """Test de consultation des colis assignés"""
        # Créer les données nécessaires
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        db_livreur = Livreur(**sample_livreur_data)
        test_db.add(db_livreur)
        test_db.commit()
        
        # Créer et assigner plusieurs colis
        for i in range(3):
            colis_data = sample_colis_data.copy()
            colis_data["description"] = f"Colis {i}"
            colis_data["id_client_expediteur"] = db_client.id
            colis_data["id_destinataire"] = db_dest.id
            colis_response = client.post("/colis/", json=colis_data)
            colis_id = colis_response.json()["id"]
            
            assignment_data = {
                "colis_id": colis_id,
                "livreur_id": db_livreur.id
            }
            client.post("/assignments/", json=assignment_data)
        
        # Récupérer tous les colis assignés
        response = client.get("/assignments/assigned")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        for colis in data:
            assert colis["id_livreur"] == db_livreur.id
    
    def test_get_assigned_colis_by_livreur(self, client, test_db, sample_colis_data,
                                           sample_client_data, sample_destinataire_data, 
                                           sample_livreur_data):
        """Test de consultation des colis assignés filtrés par livreur"""
        # Créer les données nécessaires
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        # Créer deux livreurs
        livreur1_data = sample_livreur_data.copy()
        livreur1_data["nom"] = "Livreur1"
        db_livreur1 = Livreur(**livreur1_data)
        test_db.add(db_livreur1)
        
        livreur2_data = sample_livreur_data.copy()
        livreur2_data["nom"] = "Livreur2"
        db_livreur2 = Livreur(**livreur2_data)
        test_db.add(db_livreur2)
        test_db.commit()
        
        # Créer et assigner des colis à différents livreurs
        for i in range(2):
            colis_data = sample_colis_data.copy()
            colis_data["description"] = f"Colis Livreur1 {i}"
            colis_data["id_client_expediteur"] = db_client.id
            colis_data["id_destinataire"] = db_dest.id
            colis_response = client.post("/colis/", json=colis_data)
            colis_id = colis_response.json()["id"]
            
            assignment_data = {
                "colis_id": colis_id,
                "livreur_id": db_livreur1.id
            }
            client.post("/assignments/", json=assignment_data)
        
        colis_data = sample_colis_data.copy()
        colis_data["description"] = "Colis Livreur2"
        colis_data["id_client_expediteur"] = db_client.id
        colis_data["id_destinataire"] = db_dest.id
        colis_response = client.post("/colis/", json=colis_data)
        colis_id = colis_response.json()["id"]
        
        assignment_data = {
            "colis_id": colis_id,
            "livreur_id": db_livreur2.id
        }
        client.post("/assignments/", json=assignment_data)
        
        # Filtrer par livreur1
        response = client.get(f"/assignments/assigned?livreur_id={db_livreur1.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        for colis in data:
            assert colis["id_livreur"] == db_livreur1.id
    
    def test_get_unassigned_colis(self, client, test_db, sample_colis_data,
                                  sample_client_data, sample_destinataire_data, 
                                  sample_livreur_data):
        """Test de consultation des colis non assignés"""
        # Créer les données nécessaires
        db_client = ClientExpediteur(**sample_client_data)
        test_db.add(db_client)
        test_db.commit()
        
        db_dest = Destinataire(**sample_destinataire_data)
        test_db.add(db_dest)
        test_db.commit()
        
        db_livreur = Livreur(**sample_livreur_data)
        test_db.add(db_livreur)
        test_db.commit()
        
        # Créer des colis assignés et non assignés
        for i in range(2):
            colis_data = sample_colis_data.copy()
            colis_data["description"] = f"Colis Non Assigné {i}"
            colis_data["id_client_expediteur"] = db_client.id
            colis_data["id_destinataire"] = db_dest.id
            client.post("/colis/", json=colis_data)
        
        # Créer un colis assigné
        colis_data = sample_colis_data.copy()
        colis_data["description"] = "Colis Assigné"
        colis_data["id_client_expediteur"] = db_client.id
        colis_data["id_destinataire"] = db_dest.id
        colis_response = client.post("/colis/", json=colis_data)
        colis_id = colis_response.json()["id"]
        
        assignment_data = {
            "colis_id": colis_id,
            "livreur_id": db_livreur.id
        }
        client.post("/assignments/", json=assignment_data)
        
        # Récupérer les colis non assignés
        response = client.get("/assignments/unassigned")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        for colis in data:
            assert colis["id_livreur"] is None
