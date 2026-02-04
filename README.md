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

---

## Git & GitHub

**Repo erstellen und pushen (wenn du mit GitHub CLI arbeitest):**

1. Einmal anmelden (falls nötig): `gh auth login -h github.com`
2. Repo erstellen und pushen:
   ```bash
   gh repo create dataSciene_2026 --private --source=. --remote=origin --push
   ```
   Für ein öffentliches Repo: `--public` statt `--private`.

**Oder manuell:**

1. Auf [github.com/new](https://github.com/new) ein neues Repo anlegen (z. B. `dataSciene_2026`), **ohne** README/`.gitignore` zu erstellen.
2. Remote hinzufügen und pushen:
   ```bash
   git remote add origin https://github.com/DEIN_USERNAME/dataSciene_2026.git
   git push -u origin main
   ```
