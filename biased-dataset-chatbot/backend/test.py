import pandas as pd

original = pd.read_csv('vehicules_transport_original_20260111_004715.csv')
biased = pd.read_csv('vehicules_transport_biased_20260111_004715.csv')

print(f"Taille original : {len(original)}")  # 1000
print(f"Taille biaisé : {len(biased)}")      # ~850

print(f"\nMoyenne prix original : {original['prix_unitaire'].mean():.2f}")
print(f"Moyenne prix biaisé : {biased['prix_unitaire'].mean():.2f}")  # Plus élevé !

print(f"\nMin prix original : {original['prix_unitaire'].min():.2f}")
print(f"Min prix biaisé : {biased['prix_unitaire'].min():.2f}")  # Seuil plus haut