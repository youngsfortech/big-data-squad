#  Éditeur Malagasy Intelligent

Éditeur de texte augmenté par l'Intelligence Artificielle pour la langue Malgache. Projet développé dans le cadre d'études en Traitement Automatique des Langues (TAL).


##  Fonctionnalités

###  Vérification Orthographique Intelligente
- Détection automatique des erreurs d'orthographe
- Suggestions de corrections basées sur l'algorithme de distance de Levenshtein
- Remplacement en un clic des mots incorrects
- Support des règles morphologiques du malagasy

###  Analyse de Sentiment
- Classification automatique du ton (positif, négatif, neutre)
- Score de sentiment avec visualisation graphique
- Comptage et identification des mots positifs/négatifs
- Basé sur un lexique malagasy annoté

###  Analyse Linguistique Avancée
Analyse mot par mot en sélectionnant simplement le texte :
- **Lemmatisation** : Extraction de la racine et identification des affixes (préfixes, suffixes)
- **Traduction bilingue** : Malagasy ↔ Français
- **Validation phonotactique** : Vérification de la structure phonétique selon les règles du malagasy
- **Graphe de connaissances** : Relations sémantiques et concepts liés

###  Statistiques en Temps Réel
- Compteur de mots et caractères
- Nombre d'erreurs détectées
- Taux de précision orthographique
- Métriques de qualité du texte

###  Technologies IA Utilisées
- **NLP (Natural Language Processing)** : Tokenisation, lemmatisation, analyse morphologique
- **Algorithmes de distance** : Levenshtein pour suggestions orthographiques
- **Modèles n-gram** : Prédiction et validation de séquences de mots
- **Graphes de connaissances** : Relations sémantiques entre concepts
- **Analyse de sentiment** : Classification basée sur lexique

##  Équipe de Développement

| Membre | Rôle |
|--------|------|
| **RANDRIAMANANTENA Tafitasoa Fabrice** | Développeur Full-Stack, Architecte Système, Spécialiste TAL |

**Contributions :**
- Architecture complète du système (Frontend + Backend)
- Implémentation des algorithmes de TAL
- Développement de l'interface utilisateur
- Collecte et structuration des données linguistiques
- Documentation technique
- Tests et optimisations

##  Structure du Projet

```
big-data-squad/
├── README.md                    # Ce fichier
├── frontend/                    # Interface utilisateur
│   ├── README.md               # Documentation frontend
│   ├── index.html
│   ├── index.css
│   └── js/
│       ├── icons.js
│       ├── apiService.js
│       ├── utils.js
│       ├── editorHooks.js
│       └── app.js
└── backend/                    # API et traitement
    ├── README.md               # Documentation backend
    ├── main.py
    ├── malagasy_base_data.py
    ├── scraper.py
    ├── setup_data.py
    ├── requirements.txt
    └── data/
        ├── malagasy_dictionary.json
        ├── bigram_model.json
        ├── word_frequencies.json
        └── corpus_sample.txt
```

##  Installation Rapide

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python3 setup_data.py
uvicorn main:app --reload
```

### 2. Frontend
```bash
cd frontend
python -m http.server 8080
# Ouvrir http://localhost:8080
```

**Documentation détaillée :**
- **Frontend** : Voir `frontend/README.md`
- **Backend** : Voir `backend/README.md`

## Fonctionnalités IA - Détails Techniques

### 1. Correction Orthographique
**Algorithme** : Distance de Levenshtein + Modèle n-gram
- Calcul de similarité entre mots
- Suggestions classées par pertinence
- Prise en compte du contexte via bigrams
- Seuil de distance adaptatif

### 2. Lemmatisation
**Méthode** : Analyse morphologique par règles
- Identification des préfixes (maha-, mi-, man-, etc.)
- Extraction de la racine
- Support des formes dérivées
- Basé sur la morphologie du malagasy

### 3. Analyse de Sentiment
**Approche** : Lexique + Pondération
- Dictionnaire de mots positifs/négatifs
- Score calculé sur base de fréquences
- Classification en 3 catégories
- Normalisation des scores

### 4. Validation Phonotactique
**Règles** : Contraintes phonologiques du malagasy
- Vérification des séquences de consonnes
- Validation des structures syllabiques
- Détection des combinaisons impossibles

### 5. Graphe de Connaissances
**Structure** : Relations sémantiques
- Relations synonymiques
- Relations taxonomiques (hyperonymes/hyponymes)
- Relations thématiques
- Navigation interactive

### 6. Traduction
**Méthode** : Dictionnaire bilingue enrichi
- Base de 1000+ paires de traduction
- Extension via scraping Wikipedia
- Support contexte via exemples

##  Bibliographie

### Sources de Données

#### Corpus et Dictionnaires
- **Wikipédia malgache** (mg.wikipedia.org) - Articles encyclopédiques
- **Teny Malgache** (tenymalagasy.org) - Dictionnaire malgache-français
- **Rakibolane** (rakibolana.org) - Dictionnaire unilingue
- **Wiktionnaire malgache** (mg.wiktionary.org) - Dictionnaire collaboratif

### Technique de documentation

#### Cadres et Bibliothèques
- **Rapide API** : https://fastapi.tiangolo.com - Framework API Python moderne
- **Réagir** : https://react.dev - Bibliothèque UI JavaScript
- **Quill.js** : https://quilljs.com - Éditeur de texte riche
- **Demandes** : https://requests.readthedocs.io - HTTP pour Python
- **BelleSoupe4** : https://www.crummy.com/software/BeautifulSoup - Analyseur HTML

#### Algorithmes
- Algorithme de Wagner-Fischer pour la distance de Levenshtein
- Modèles linguistiques N-gram (Manning et Schütze, 1999)
- Analyseur des sentiments basés sur le lexique

### Normes et standards
- **ISO 639-3** : mlg (Code langue malgache)
- **Unicode** : Soutien complet des carrières malgaches
- **API REST** : Architecture de l'API backend

## Technologies Utilisées

### Backend
- Python 3.8+
- FastAPI (API REST)
- Demandes (HTTP)
- BeautifulSoup4 (Scraping)

### Front-end
- Réagir 18
- Quill.js
- Babel autonome
- CSS3

### Algorithmes IA
- Distance de Levenshtein
- Modèles n-gram
- Analyseur le lexical
- Graphes sémantiques

## Licence

Licence MIT - Libre d'utilisation à des fins éducatives et de recherche.

## Contributions

Les contributions sont les bienvenues ! Pour contribuer :
1. Fourche le projet
2. Créez une branche (`git checkout -b fonctionnalité/amélioration`)
3. Engagez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Poussez vers la branche (`fonctionnalitéalité/édition de l'origine git push`)
5. Ouvrez une Pull Request

## Contact

**Développeur** : Fabrice <br>
**Projet** : Éditeur Malgache Intelligent <br>
**Institution** : ISPM (Institut Supérieur Polytechnique de Madagascar)

---

**Note** : Pour les détails techniques d'implémentation, consultez les README spécifiques dans les dossiers `interface/` et `backend/`.
