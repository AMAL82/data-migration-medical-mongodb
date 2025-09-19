import pandas as pd
from pymongo import MongoClient, ASCENDING
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Charger les variables du .env
load_dotenv()

# Récupération des variables d'environnement
user = quote_plus(str(os.getenv("MONGO_USER", "")))
password = quote_plus(str(os.getenv("MONGO_PASSWORD", "")))
host = os.getenv("MONGO_HOST", "mongodb")
port = os.getenv("MONGO_PORT", "27017")
db_name = os.getenv("MONGO_DB", "healthcare")
csv_file = os.getenv("CSV_FILE", "/data/ready_healthcare_dataset.csv")

MONGO_URI = f"mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource=admin"

def migration():
    try:
        # Connexion MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        collection = db["patient_healthcare"]
        print("✅ Connexion MongoDB réussie !")

        # Lecture du CSV
        df = pd.read_csv(csv_file)
        print(f"📂 Fichier CSV chargé : {len(df)} lignes, {len(df.columns)} colonnes.")

        # Typage (adapter selon ton dataset)
        df['Name'] = df['Name'].astype(str)
        df['Age'] = df['Age'].astype(int)
        df['Gender'] = df['Gender'].astype(str)
        df['Blood Type'] = df['Blood Type'].astype(str)
        df['Medical Condition'] = df['Medical Condition'].astype(str)
        df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
        df['Doctor'] = df['Doctor'].astype(str)
        df['Hospital'] = df['Hospital'].astype(str)
        df['Insurance Provider'] = df['Insurance Provider'].astype(str)
        df['Billing Amount'] = df['Billing Amount'].astype(float)
        df['Room Number'] = df['Room Number'].astype(int)
        df['Admission Type'] = df['Admission Type'].astype(str)
        df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
        df['Medication'] = df['Medication'].astype(str)
        df['Test Results'] = df['Test Results'].astype(str)

        # Conversion en dictionnaires
        data = df.to_dict(orient="records")

        # Insertion dans MongoDB
        if data:
            collection.delete_many({})  # nettoyer avant réinsertion
            collection.insert_many(data)
            print(f"✅ {len(data)} documents insérés dans 'patient_healthcare'.")

        # Création d'index pertinents
        collection.create_index([("Name", ASCENDING)], name="idx_name")
        collection.create_index([("Doctor", ASCENDING)], name="idx_doctor")
        collection.create_index([("Hospital", ASCENDING)], name="idx_hospital")
        collection.create_index([("Date of Admission", ASCENDING)], name="idx_admission_date")
        collection.create_index([("Medical Condition", ASCENDING)], name="idx_medical_condition")

        print("✅ Index créés avec succès.")

    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")

if __name__ == "__main__":
    migration()