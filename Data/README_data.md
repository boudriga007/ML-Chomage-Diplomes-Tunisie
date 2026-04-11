# 📊 Dataset — ENPE 2017 (INS Tunisie)

## Pourquoi le dataset n'est pas dans ce repository ?

Le fichier source `enpe2t17fipuf.sas7bdat` pèse **69.3 MB**, ce qui dépasse la limite GitHub (25 MB). Il n'est donc pas inclus directement.

---

## Comment télécharger le dataset ?

### Option 1 — Téléchargement direct depuis le portail INS

1. Aller sur : **http://nada.ins.tn**
2. Dans la barre de recherche, taper : `ENPE 2017`
3. Cliquer sur : **Enquête Nationale sur la Population et l'Emploi 2017**
4. Aller dans l'onglet **"Données"** ou **"Microdata"**
5. Télécharger le fichier : `enpe2t17fipuf.sas7bdat`

### Option 2 — Page officielle INS

URL directe :
```
https://www.ins.tn/enquetes/enquete-nationale-sur-la-population-et-lemploi-2017
```

---

## Où placer le fichier ?

Après téléchargement, placer le fichier dans le dossier racine du projet :

```
ML-Chomage-Diplomes-Tunisie/
├── enpe2t17fipuf.sas7bdat    ← ICI
├── notebooks/
├── src/
└── ...
```

---

## Description du dataset

| Paramètre | Valeur |
|---|---|
| **Nom** | Enquête Nationale Population et Emploi 2017 |
| **Organisme** | Institut National de la Statistique (INS) Tunisie |
| **Année** | 2017 |
| **Format** | SAS (.sas7bdat) |
| **Taille** | 69.3 MB |
| **Lignes** | 452 928 individus |
| **Colonnes** | 20 variables |
| **Couverture** | 24 gouvernorats tunisiens |

---

## Variables principales utilisées dans le projet

| Variable | Label INS | Type |
|---|---|---|
| `V_9_10_i` | Gouvernorat | Catégorielle |
| `V_9_11_1` | Milieu (urbain/rural) | Binaire |
| `V_1_203_i` | Lien de parenté | Catégorielle |
| `V_1_204_i` | Sexe | Binaire |
| `V_1_205_i` | Situation matrimoniale | Catégorielle |
| `V_210tr` | Âge | Numérique |
| `V_1_225_i` | Niveau d'instruction | Ordinale |
| `V_4_321_i` | Secteur d'activité | Catégorielle |
| `V_4_325_i` | Catégorie socioprofessionnelle | Catégorielle |
| `V_0_244_i` | **Situation dans l'emploi (CIBLE)** | Catégorielle |
| `weight` | Pondération INS | Numérique |

---

## Codes de la variable cible V_0_244_i

| Code | Signification | Nb individus |
|---|---|---|
| `1` | Chômeur | 69 220 |
| `2` | Employé (actif occupé) | 96 198 |
| `3` | Inactif | 129 993 |
| `4` | Moins de 15 ans (exclu) | — |
| `9` | Non déclaré (exclu) | — |

---

## Librairie nécessaire pour lire le fichier

```bash
pip install pyreadstat
```

```python
import pyreadstat
df, meta = pyreadstat.read_sas7bdat("enpe2t17fipuf.sas7bdat")
print(df.shape)  # (452928, 20)
```
