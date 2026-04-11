# 🎓 Prédiction du Chômage des Diplômés Tunisiens
## Projet Machine Learning End-to-End — ENPE 2017

![Python](https://img.shields.io/badge/Python-3.12-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-orange)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-1.5-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52-red)

---

## 👤 Auteur
**Boudriga Ahmed**  
Projet ML — 2025–2026

---

## 📋 Description du Projet

La Tunisie souffre d'un paradoxe économique majeur : le taux de chômage des diplômés du supérieur atteint **23,7 %** (INS, T2 2023), soit le double de la moyenne nationale. Ce phénomène touche particulièrement les jeunes des régions intérieures et les femmes diplômées.

**Objectif :** Construire un modèle de classification supervisée capable de prédire le statut d'emploi d'un diplômé tunisien — **Employé**, **Chômeur** ou **Inactif** — à partir de ses caractéristiques socio-démographiques issues de l'enquête ENPE 2017.

---

## 📊 Dataset

| Paramètre | Valeur |
|---|---|
| **Source** | INS Tunisie — Enquête Nationale Population et Emploi 2017 |
| **URL** | https://www.ins.tn/enquetes/enquete-nationale-sur-la-population-et-lemploi-2017 |
| **Format** | SAS (.sas7bdat) |
| **Lignes** | 452 928 individus |
| **Colonnes** | 20 variables |
| **Après filtrage** | 295 411 individus (âge ≥ 15, codes valides) |

> ⚠️ Le dataset brut n'est pas inclus dans ce repository (taille > 69 MB).  
> Voir `data/README_data.md` pour les instructions de téléchargement.

---

## 🎯 Problématique ML

**Type :** Classification supervisée multi-classes (3 classes)

**Variable cible :** Statut dans l'emploi (`V_0_244_i`)
- `0` = Employé (actif occupé)
- `1` = Chômeur (cherche un emploi)
- `2` = Inactif (hors marché du travail)

**Features utilisées (14 variables) :**

| Variable | Description |
|---|---|
| `V_9_10_i` | Gouvernorat (24 régions) |
| `V_9_11_1` | Milieu (urbain/rural) |
| `V_1_203_i` | Lien de parenté |
| `V_1_204_i` | Sexe |
| `V_1_205_i` | Situation matrimoniale |
| `V_210tr` | Âge |
| `V_1_225_i` | Niveau d'instruction |
| `V_4_321_i` | Secteur d'activité |
| `V_4_325_i` | Catégorie socioprofessionnelle |
| `region_interieure` | FE : région intérieure (0/1) |
| `groupe_age` | FE : groupe d'âge (0–3) |
| `diplome_superieur` | FE : diplômé supérieur (0/1) |
| `femme_region_int` | FE : femme × région intérieure |
| `jeune_diplome` | FE : jeune diplômé < 35 ans |

---

## 🗂️ Structure du Repository

```
ML-Chomage-Diplomes-Tunisie/
│
├── data/
│   └── README_data.md           # Instructions téléchargement ENPE 2017
│
├── notebooks/
│   ├── 01_Phase1_Chargement.ipynb       # Chargement et découverte
│   ├── 02_Phase2_EDA.ipynb              # Analyse exploratoire
│   ├── 03_Phase3_Preprocessing.ipynb    # Preprocessing + Feature Engineering
│   ├── 04_Phase4_Modelisation.ipynb     # 5 modèles + comparaison
│   ├── 05_Phase5_Interpretabilite.ipynb # Feature Importance + évaluation finale
│   └── 06_Amelioration_Tentative.ipynb  # Tentative amélioration (rejetée)
│
├── src/
│   └── app.py                   # Application Streamlit
│
├── requirements.txt             # Dépendances Python
├── README.md                    # Ce fichier
├── Presentation.pdf             # Slides de soutenance
└── .gitignore                   # Fichiers ignorés par Git
```

---

## 🔬 Processus Machine Learning

```
Phase 1 → Chargement ENPE 2017 (452 928 individus, format SAS)
Phase 2 → EDA : 8 graphiques, paradoxe diplôme, analyse territoriale
Phase 3 → Preprocessing : filtrage, FE (14 features), SMOTE, split 80/20
Phase 4 → 5 modèles : LR, RF, XGBoost, SVM, KNN — XGBoost meilleur
Phase 5 → Feature Importance (3 métriques XGBoost), évaluation finale
Phase 6 → Tentative 2 classes vs 3 classes → modèle Phase 4 retenu
```

---

## 📈 Résultats

### Comparaison des 5 modèles

| Modèle | Accuracy | F1-macro | Recall Chômeur |
|---|---|---|---|
| **XGBoost** ← | **0.660** | **0.651** | 0.651 |
| Logistic Regression | 0.626 | 0.620 | 0.739 |
| Random Forest | 0.621 | 0.613 | 0.702 |
| SVM (Linear) | 0.629 | 0.608 | 0.659 |
| KNN | 0.589 | 0.580 | 0.596 |

### Performances par classe — XGBoost final

| Classe | Precision | Recall | F1-score |
|---|---|---|---|
| Employé | 0.52 | 0.53 | 0.53 |
| **Chômeur** | **0.65** | **0.72** | **0.69** |
| Inactif | 0.76 | 0.70 | 0.73 |
| **Moyenne macro** | | | **0.651** |

### Interprétation des scores

Un F1-macro de **0.651** est un score honnête et réaliste pour ce problème car :
- 3 classes naturellement déséquilibrées dans les données réelles
- Features socio-démographiques limitées (pas de données salariales)
- La classe "Employé" est sous-représentée (21% du dataset)

---

## 🚀 Installation et Utilisation

### 1. Cloner le repository

```bash
git clone https://github.com/TonNom/ML-Chomage-Diplomes-Tunisie.git
cd ML-Chomage-Diplomes-Tunisie
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Télécharger le dataset

Voir `data/README_data.md` pour les instructions complètes.

### 4. Lancer les notebooks dans l'ordre

```bash
jupyter notebook notebooks/01_Phase1_Chargement.ipynb
```

### 5. Lancer l'application Streamlit

```bash
streamlit run src/app.py
```

---

## 🛠️ Technologies Utilisées

| Librairie | Version | Usage |
|---|---|---|
| Python | 3.12 | Langage principal |
| pandas | 2.x | Manipulation données |
| numpy | 1.26 | Calcul numérique |
| scikit-learn | 1.5 | ML pipeline |
| xgboost | 2.0.3 | Modèle final |
| imbalanced-learn | 0.12 | SMOTE |
| matplotlib | 3.9 | Visualisations |
| seaborn | 0.13 | Visualisations |
| streamlit | 1.52 | Application web |
| pyreadstat | 1.3 | Lecture SAS |
| joblib | 1.4 | Sauvegarde modèles |

---

## 📁 Fichiers Modèle

Après exécution des notebooks, les fichiers suivants sont générés :

| Fichier | Contenu |
|---|---|
| `modele_final.pkl` | Modèle XGBoost entraîné |
| `features.pkl` | Liste des 14 features |
| `scaler.pkl` | StandardScaler ajusté |
| `imputer.pkl` | SimpleImputer ajusté |

---

## 📚 Sources

- **Dataset :** Institut National de la Statistique (INS) Tunisie — ENPE 2017
- **Référence :** http://nada.ins.tn
- **Cahier des charges :** Projet ML End-to-End 2025–2026
