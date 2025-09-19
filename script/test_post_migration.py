import os
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
from urllib.parse import quote_plus
load_dotenv()

# Configuration/connexion
user = quote_plus(str(os.getenv("MONGO_USER", "")))
password = quote_plus(str(os.getenv("MONGO_PASSWORD", "")))
host = os.getenv("MONGO_HOST", "mongodb")
port = os.getenv("MONGO_PORT", "27017")
db_name = os.getenv("MONGO_DB", "healthcare")

MONGO_URI = f"mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource=admin"
DB_NAME = os.getenv("MONGO_DB", "healthcare")
COLLECTION_NAME = "patient_healthcare"

# Champs attendus + types attendus (Python)
expected_fields = {
    "Name": str,
    "Age": int,
    "Gender": str,
    "Blood Type": str,
    "Medical Condition": str,
    "Date of Admission": "datetime",
    "Doctor": str,
    "Hospital": str,
    "Insurance Provider": str,
    "Billing Amount": float,
    "Room Number": int,
    "Admission Type": str,
    "Discharge Date": "datetime",
    "Medication": str,
    "Test Results": str
}

def run_tests():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    print("\n=== Vérification intégrité des données ===")

    # ✅ 1. Vérifier présence des champs
    print("\nVérification des champs présents dans un document :")
    sample_doc = collection.find_one()
    if sample_doc:
        print("Champs trouvés :", list(sample_doc.keys()))
        for field in expected_fields.keys():
            if field not in sample_doc:
                print(f"❌ Champ manquant : {field}")
        print("✅ Tous les champs attendus sont présents.")
    else:
        print("❌ Aucun document trouvé dans la collection.")

    # ✅ 2. Vérifier valeurs manquantes
    print("\nVérification des valeurs manquantes :")
    docs = list(collection.find())
    df = pd.DataFrame(docs)
    missing = df.isnull().sum()
    print(missing)

    # ✅ 3. Vérifier doublons dataframe
    print("\nVérification des doublons :")
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"❌ {duplicates} doublons trouvés")
    else:
        print("✅ Pas de doublons.")

    # ✅ 4. Vérifier doublons directement dans MongoDB
    print("\nVérification des doublons dans MongoDB :")
    pipeline = [
        {"$group": {
            "_id": {field: f"${field}" for field in expected_fields.keys()},
            "count": {"$sum": 1}
        }},
        {"$match": {"count": {"$gt": 1}}}
    ]
    mongo_duplicates = list(collection.aggregate(pipeline))

    if mongo_duplicates:
        print(f"❌ {len(mongo_duplicates)} groupes de doublons trouvés dans MongoDB.")
        for dup in mongo_duplicates[:5]:  # afficher seulement 5 max
            print(f"Exemple doublon: {dup['_id']} (x{dup['count']})")
    else:
        print("✅ Pas de doublons détectés dans MongoDB.")



    # ✅ 5. Vérifier types
    print("\nVérification des types (exemple sur 5 documents) :")
    sample_docs = collection.find().limit(5)
    for i, doc in enumerate(sample_docs, start=1):
        print(f"\n--- Document {i} ---")
        for field, expected_type in expected_fields.items():
            value = doc.get(field, None)
            if value is None:
                print(f"{field}: ❌ Valeur manquante")
                continue

            real_type = type(value).__name__

            # Gestion spéciale pour les dates
            if expected_type == "datetime":
                if real_type == "datetime":
                    print(f"{field}: ✅ {value} ({real_type})")
                else:
                    print(f"{field}: ❌ {value} (Type trouvé: {real_type}, attendu: datetime)")
            else:
                if isinstance(value, expected_type):
                    print(f"{field}: ✅ {value} ({real_type})")
                else:
                    print(f"{field}: ❌ {value} (Type trouvé: {real_type}, attendu: {expected_type.__name__})")

    print("\n=== Tests terminés ===")

if __name__ == "__main__":
    run_tests()