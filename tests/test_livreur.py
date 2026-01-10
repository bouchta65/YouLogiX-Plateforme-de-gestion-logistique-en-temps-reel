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


class TestLivreurController:
    """Tests pour les fonctions du contrôleur Livreur"""
    
    def test_create_livreur_in_db(self, test_db, sample_livreur_data):
        """Test de création d'un livreur dans la base de données"""
        from app.controllers.livreur_controller import create_livreur
        from app.schemas.livreur import LivreurCreate
        
        livreur_create = LivreurCreate(**sample_livreur_data)
        db_livreur = create_livreur(test_db, livreur_create)
        
        assert db_livreur.id is not None
        assert db_livreur.nom == sample_livreur_data["nom"]
        assert db_livreur.prenom == sample_livreur_data["prenom"]
        assert db_livreur.telephone == sample_livreur_data["telephone"]
        assert db_livreur.vehicule == sample_livreur_data["vehicule"]
    
    def test_get_livreurs_from_db(self, test_db, sample_livreur_data):
        """Test de récupération de tous les livreurs de la base de données"""
        from app.controllers.livreur_controller import create_livreur, get_livreurs
        from app.schemas.livreur import LivreurCreate
        
        # Créer plusieurs livreurs
        for i in range(3):
            livreur_data = sample_livreur_data.copy()
            livreur_data["nom"] = f"Livreur{i}"
            livreur_create = LivreurCreate(**livreur_data)
            create_livreur(test_db, livreur_create)
        
        all_livreurs = get_livreurs(test_db)
        
        assert len(all_livreurs) == 3
    
    def test_update_livreur_in_db(self, test_db, sample_livreur_data):
        """Test de mise à jour d'un livreur dans la base de données"""
        from app.controllers.livreur_controller import create_livreur, update_livreur
        from app.schemas.livreur import LivreurCreate, LivreurUpdate
        
        # Créer un livreur
        livreur_create = LivreurCreate(**sample_livreur_data)
        db_livreur = create_livreur(test_db, livreur_create)
        
        # Mettre à jour le livreur
        update_data = LivreurUpdate(nom="Nom Mis à Jour", vehicule="Voiture", zone_assignee="Zone Sud")
        updated_livreur = update_livreur(test_db, db_livreur.id, update_data)
        
        assert updated_livreur.nom == "Nom Mis à Jour"
        assert updated_livreur.vehicule == "Voiture"
        assert updated_livreur.zone_assignee == "Zone Sud"
    
    def test_delete_livreur_from_db(self, test_db, sample_livreur_data):
        """Test de suppression d'un livreur de la base de données"""
        from app.controllers.livreur_controller import create_livreur, delete_livreur, get_livreur_by_id
        from app.schemas.livreur import LivreurCreate
        
        # Créer un livreur
        livreur_create = LivreurCreate(**sample_livreur_data)
        db_livreur = create_livreur(test_db, livreur_create)
        livreur_id = db_livreur.id
        
        # Supprimer le livreur
        deleted_livreur = delete_livreur(test_db, livreur_id)
        
        assert deleted_livreur.id == livreur_id
        
        # Vérifier que le livreur n'existe plus
        assert get_livreur_by_id(test_db, livreur_id) is None

