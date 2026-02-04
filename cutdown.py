import pandas as pd

# CSV-Datei einlesen
input_file = 'online_retail_II.csv'
output_file = 'online_retail_II_cutdown.csv'

# Nur die ersten 100.000 Zeilen einlesen (plus Header)
df = pd.read_csv(input_file, nrows=100000)

# Auf 100.000 Zeilen beschränkte Datei speichern
df.to_csv(output_file, index=False)

print(f"Dataset erfolgreich auf {len(df):,} Zeilen beschränkt.")
print(f"Neue Datei gespeichert als: {output_file}")
