import pandas as pd

# Chemin du fichier CSV
CSV_FILE = "data/healthcare_dataset.csv"

# Lire le CSV dans un DataFrame
df = pd.read_csv(CSV_FILE)

# Afficher le nombre de lignes et de colonnes
print(f"Lignes : {df.shape[0]}, Colonnes : {df.shape[1]}")

# Afficher les premières lignes du DataFrame
print(df.head())

# Afficher les informations sur le DataFrame
print(df.info())

# Afficher le nombre de doublons
print(f"Doublons : {df.duplicated().sum()}")

# Afficher les lignes dupliquées
print("\nLignes dupliquées :\n")
doublons = df[df.duplicated()]
print(doublons)

# Suppression des doublons
df_sans_doublons = df.drop_duplicates()

# Afficher le nombre de lignes après suppression des doublons & vérification
print(f"\nAprès suppression des doublons : Lignes : {df_sans_doublons.shape[0]}, Colonnes : {df_sans_doublons.shape[1]}")
print(f"Doublons : {df_sans_doublons.duplicated().sum()}")

# Enregistrer dans un nouveau CSV
df_sans_doublons.to_csv("data/ready_healthcare_dataset.csv", index=False)

print("Fichier enregistré : ready_healthcare_dataset.csv")