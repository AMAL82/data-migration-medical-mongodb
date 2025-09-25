# 📄 README.md - Projet de Migration de Données Médicales vers MongoDB

### 🩺 Introduction

Ce projet a pour objectif de fournir une solution scalable pour la gestion de données médicales à un client de **DataSoluTech**.  
La mission principale est de **migrer un dataset médical de patients vers une base de données MongoDB**, en utilisant **Docker** pour la conteneurisation et l'automatisation.  

Ce travail inclut également une exploration des options de déploiement de MongoDB sur **AWS** afin de proposer une solution Big Data durable et performante.

---

### ⚙️ Architecture du Projet

Le projet est organisé autour de plusieurs composants clés :

* **Scripts Python** : trois scripts sont utilisés pour la préparation, la migration et la vérification des données.  
* **MongoDB en conteneur** : l'instance de MongoDB est exécutée dans un conteneur Docker, assurant un environnement isolé et portable.  
* **Docker Compose** : le fichier `docker-compose.yml` orchestre le lancement de MongoDB et des scripts nécessaires.  
* **Fichier `requirements.txt`** : liste les dépendances Python nécessaires pour exécuter les scripts.
---

### 🚀 Scripts de la mission

Le répertoire **`script/`** contient les fichiers suivants :

---

#### 📌 `data_cleaning.py`

* Dédié au **nettoyage et à la transformation des données**.  
* Lit le fichier **CSV brut** et effectue :  
  - standardisation des formats,  
  - traitement des doublons,  
  - préparation des données avant insertion.  
* ➡️ garantir la qualité et l'intégrité des données importées.

---

#### 📌 `migration.py`

* Script **principal** de la mission.  
* Chargé de l'**importation des données nettoyées** dans la collection **`patients`**.  
* Fonctionnalités :  
  - connexion à la base MongoDB,  
  - insertion des documents dans la collection cible.  

---

#### 📌 `test_post_migration.py`

* Script de **vérification après migration**.  
* Contrôles effectués :  
  - nombre total de documents,  
  - formatage de certains champs,  
  - détection d’erreurs ou anomalies.  
* ➡️ Garantit la fiabilité des données migrées.

---

### 🚀 Comment démarrer

#### ✅ Prérequis

- [Docker](https://www.docker.com/)  
- [Docker Compose](https://docs.docker.com/compose/)  

#### 📋 Instructions

1. **Cloner le dépôt GitHub** :
   ```bash
   git clone https://github.com/AMAL82/data-migration-medical-mongodb.git
   cd data-migration-medical-mongodb
   ```

2. **Lancer la migration** :
   ```bash
   docker-compose up --build
   ```
   👉 L’option `--build` force la reconstruction de l’image Docker avec vos dernières modifications.

3. **Vérifier les données** :
   - Connexion par défaut : `mongodb://localhost:27017/`  
   - Vérifier la collection `patient_healthcare` dans la base `healthcare`.  

---

### 📂 Schéma de la base de données

Les données sont importées dans la collection **`patient_healthcare`** de la base **`healthcare`**.  

Exemple de document :  

{
  "_id": { "$oid": "..." },
  "id": "...",
  "gender": "...",
  "age": ...,
  "hypertension": ...,
  "heart_disease": ...,
  "ever_married": "...",
  "work_type": "...",
  "Residence_type": "...",
  "avg_glucose_level": ...,
  "bmi": ...,
  "smoking_status": "...",
  "stroke": ...
}
```

---

### 🔒 Sécurité et Authentification

Un système d’authentification MongoDB a été mis en place :  

- **Utilisateur admin** :  
  - droits root,  
  - gestion complète de la base de données.  

- **Utilisateur app_user** :  
  - permissions limitées (`readWrite`, `dbAdmin`),  
  - adapté à une application cliente.  

👉 Les identifiants utilisateurs sont gérés via des **variables d’environnement** dans `docker-compose.yml`.  

---

### 📌 Améliorations futures

- Déploiement d’un cluster MongoDB sur AWS  

---
