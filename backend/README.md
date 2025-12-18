# Structure des Données - Backend

## Architecture des Fichiers

```
backend/
├── malagasy_base_data.py      # Données de base centralisées
├── scraper.py                 # Script de scraping
├── setup_data.py              # Script d'initialisation
├── main.py                    # Backend FastAPI
├── requirements.txt           # Dépendances Python
└── data/                      # Données générées
    ├── malagasy_dictionary.json
    ├── bigram_model.json
    ├── word_frequencies.json
    └── corpus_sample.txt
```

## Description des Fichiers

### 1. `malagasy_base_data.py`
**Fichier central des données de base**

Contient :
- **BASE_DICTIONARY** : 200+ mots malagasy courants
- **BASE_BIGRAM_MODEL** : Modèle de prédiction bigram
- **BASE_WORD_FREQUENCIES** : Fréquences des mots
- **BASE_CORPUS_SAMPLE** : Échantillon de texte malagasy

**Utilisé par :**
- `scraper.py` → Fallback si le scraping échoue
- `setup_data.py` → Création de données minimales

**Avantages :**
- Pas de duplication de code
- Facile à maintenir et enrichir
- Réutilisable par tous les scripts

### 2. `scraper.py`
**Script de collecte de données depuis le web**

**Sources :**
- Wikipedia MG (API officielle)
- Teny Malagasy
- Rakibolana (optionnel)
- Wiktionary MG (optionnel)

**Utilisation :**
```bash
# Scraping standard
python3 scraper.py

# Le scraper utilise automatiquement malagasy_base_data.py 
# si le scraping échoue
```

### 3. `setup_data.py`
**Script d'initialisation du projet**

**Fonctionnalités :**
- Vérifie si les données existent
- Lance le scraping si nécessaire
- Crée des données minimales en fallback
- Affiche les statistiques

**Utilisation :**
```bash
# Setup interactif
python3 setup_data.py

# Force le re-scraping
python3 setup_data.py --force

# Scraping rapide
python3 setup_data.py --quick

# Toutes les sources
python3 setup_data.py --all-sources

# Données minimales uniquement
python3 setup_data.py --minimal
```

### 4. Dossier `data/`
**Données générées automatiquement**

Fichiers créés :
- `malagasy_dictionary.json` : Liste complète des mots
- `bigram_model.json` : Modèle de prédiction
- `word_frequencies.json` : Top 1000 mots fréquents
- `corpus_sample.txt` : Échantillon de texte

**Important :** Ces fichiers sont générés automatiquement. Ne pas modifier manuellement.

##  Flux de Travail

### Première Installation
```bash
# 1. Le projet démarre sans données
python3 setup_data.py

# 2. setup_data.py vérifie que data/ n'existe pas

# 3. Deux options :
#    → Scraping automatique (recommandé)
#    → Données minimales depuis malagasy_base_data.py

# 4. Les fichiers JSON sont créés dans data/

# 5. Le backend peut démarrer
uvicorn main:app --reload
```

### Enrichissement des Données
```bash
# Re-scraping pour plus de mots
python3 setup_data.py --force --all-sources

# Le scraper collecte depuis toutes les sources
# et enrichit les données existantes
```

### Modification du Dictionnaire de Base
```python
# Éditer malagasy_base_data.py
BASE_DICTIONARY = [
    # Ajouter vos mots ici
    'nouveau_mot',
    'autre_mot',
    # ...
]

# Puis régénérer
python3 setup_data.py --minimal
```

##  Personnalisation

### Ajouter des Mots de Base
Éditez `malagasy_base_data.py` :
```python
BASE_DICTIONARY = [
    # Vos mots existants...
    'mon_nouveau_mot',
    'autre_mot',
]
```

### Ajouter des Sources de Scraping
Éditez `scraper.py` :
```python
def scrape_nouvelle_source(self):
    """Votre nouveau scraper"""
    # Votre code ici
    pass
```

Puis dans `setup_data.py` :
```python
scraper.scrape_nouvelle_source()
```

##  Statistiques Typiques

Après un scraping complet :
- **Dictionnaire** : 1000-3000 mots
- **Bigram** : 500-1500 entrées
- **Fréquences** : Top 1000 mots
- **Corpus** : 50-100 articles

Avec données minimales uniquement :
- **Dictionnaire** : ~200 mots
- **Bigram** : ~20 entrées
- **Fréquences** : ~30 mots

## Dépannage

### Erreur : "Module malagasy_base_data not found"
```bash
# Assurez-vous que malagasy_base_data.py est présent
ls -la malagasy_base_data.py

# Si absent, téléchargez-le ou créez-le
```

### Erreur : "No data files found"
```bash
# Lancez le setup
python3 setup_data.py
```

### Scraping échoue (erreurs SSL/réseau)
```bash
# Utilisez les données minimales
python3 setup_data.py --minimal

# Les données de base suffiront pour tester
```

## Commandes Rapides

```bash
# Setup initial
python3 setup_data.py

# Scraping complet
python3 setup_data.py --force --all-sources

# Données minimales
python3 setup_data.py --minimal

# Lancer le serveur
uvicorn main:app --reload

# Vérifier les données
cat data/malagasy_dictionary.json | python3 -m json.tool | head
```

## Ressources

- **Wikipedia MG** : https://mg.wikipedia.org
- **Teny Malagasy** : https://tenymalagasy.org
- **Rakibolana** : https://rakibolana.org
- **Wiktionary MG** : https://mg.wiktionary.org

## Contributions

Pour enrichir le dictionnaire de base :
1. Éditez `malagasy_base_data.py`
2. Ajoutez vos mots dans les listes appropriées
3. Testez avec `python3 setup_data.py --minimal`
4. Vérifiez les fichiers générés dans `data/`

---