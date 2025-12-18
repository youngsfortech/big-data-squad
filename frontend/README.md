# Éditeur Malagasy Intelligent - Frontend

Interface web pour l'édition de texte en langue Malgache avec analyses linguistiques.

## Architecture du Projet

```
frontend/
├── index.html             # Point d'entrée HTML
├── index.css              # Styles de l'application
└── js/                    # Modules JavaScript
    ├── icons.js           # Composants SVG (13 icônes)
    ├── apiService.js      # Services API (6 endpoints)
    ├── utils.js           # Fonctions utilitaires
    ├── editorHooks.js     # Hook React personnalisé
    └── app.js             # Composant principal
```

##  Installation

### Prérequis
- Navigateur web moderne
- Backend API sur `http://localhost:8000`

### Démarrage

**Option 1 : Ouvrir directement**
```bash
open index.html  # macOS
start index.html # Windows
```

**Option 2 : Serveur local (recommandé)**
```bash
# Python
python -m http.server 8080

# Node.js
npx http-server -p 8080

# PHP
php -S localhost:8080
```

Accédez à `http://localhost:8080`

## Technologies

| Technologie | Version | Usage |
|-------------|---------|-------|
| React | 18 | Framework UI |
| Quill.js | 1.3.6 | Éditeur WYSIWYG |
| Babel Standalone | Latest | Transpilation JSX |
| CSS3 | - | Styles modernes |

**Aucune installation npm** - Dépendances via CDN.

## Structure des Modules

### `js/icons.js` → `window.Icons`
```javascript
{
  CheckIcon, SentimentIcon, DocumentIcon, BookIcon,
  DeleteIcon, ChartIcon, TranslateIcon, LinkIcon,
  SoundIcon, HappyIcon, SadIcon, NeutralIcon
}
```

### `js/apiService.js` → `window.ApiService`
```javascript
{
  spellCheck(text)                    // Vérification orthographique
  analyzeSentiment(text)              // Analyse de sentiment
  lemmatizeWord(word)                 // Lemmatisation
  getKnowledgeGraph(word)             // Graphe de connaissances
  translateWord(word, src, target)    // Traduction
  validatePhonotactics(word)          // Validation phonotactique
}
```

### `js/utils.js` → `window.Utils`
```javascript
{
  updateStats(content, results)       // Calcul statistiques
  calculateAccuracy(stats)            // Taux de précision
  getSampleText()                     // Texte d'exemple
}
```

### `js/editorHooks.js` → `window.useQuillEditor`
Hook React pour Quill.js :
```javascript
const quillRef = useQuillEditor(onTextChange, onTextSelection);
```

### `js/app.js` → `window.MalagasyEditor`
Composant principal React.

## API Requirements

Le backend doit fournir ces endpoints :

| Endpoint | Body | Réponse |
|----------|------|---------|
| `POST /spell-check` | `{text}` | `{results[], errors_found}` |
| `POST /sentiment` | `{text}` | `{sentiment, score, ...}` |
| `POST /lemmatize` | `{word}` | `{root, prefixes[]}` |
| `POST /knowledge-graph` | `{word}` | `{found, direct_relations[]}` |
| `POST /translate` | `{word, source_lang, target_lang}` | `{found, translation}` |
| `POST /validate-phonotactics` | `{word}` | `{is_valid}` |

## Configuration

### Changer l'URL du backend
Dans `js/apiService.js` :
```javascript
const API_BASE = "http://localhost:8000"; // Modifier ici
```

## Dépannage

### Backend non accessible
```
Error: Failed to fetch
```
  Vérifiez que le backend tourne sur le bon port  
  Configurez les CORS sur le backend  
  Testez : `curl http://localhost:8000/spell-check`

### Page blanche
  Ouvrez la console (F12)  
  Vérifiez l'ordre des scripts dans `index.html`  
  Assurez-vous que tous les fichiers JS sont présents

##  Notes Techniques

### Pourquoi `window.*` au lieu de `import/export` ?
Babel Standalone ne supporte pas les modules ES6 natifs. Les modules sont exportés via `window` pour la compatibilité.

### Ordre de chargement des scripts
L'ordre dans `index.html` est crucial :
1. `icons.js` - Pas de dépendances
2. `utils.js` - Pas de dépendances
3. `apiService.js` - Pas de dépendances
4. `editorHooks.js` - Utilise React
5. `app.js` - Utilise tous les modules précédents

### Ajout d'un nouveau module
```javascript
// js/monModule.js
window.MonModule = {
  maFonction: () => { ... }
};
```

```html
<!-- index.html -->
<script type="text/babel" src="./js/monModule.js"></script>
```

```javascript
// js/app.js
const { maFonction } = window.MonModule;
```