# FP-Growth & Association Rules

Projekt zur Analyse von Warenkorbdaten mit dem FP-Growth-Algorithmus und Assoziationsregeln (Online Retail II Datensatz).

## Inhalt

- **FP_Growth.py** – FP-Tree-Implementierung und Mining von häufigen Itemsets sowie Ableitung von Assoziationsregeln
- **cutdown.py** – Skript zum Erzeugen einer verkleinerten Stichprobe der Transaktionen
- **online_retail_II_cutdown.csv** – Stichprobe der Retail-Daten
- **association_rules.csv** – exportierte Assoziationsregeln

## Nutzung

```bash
python FP_Growth.py
```

Die große Rohdatei `online_retail_II.csv` ist nicht im Repo (Größenlimit). Sie kann von der Quelle heruntergeladen und lokal verwendet werden.
