"""
Backend FastAPI pour Éditeur Malagasy Intelligent
Installation: pip install fastapi uvicorn rapidfuzz nltk
Lancer: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re
from rapidfuzz import fuzz, process
import nltk
import json
import os

# Télécharger les ressources NLTK nécessaires
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

app = FastAPI(title="Malagasy AI Text Editor API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DONNÉES ET CONFIGURATION
# ============================================================================

# Combinaisons phonotactiques interdites en malagasy
INVALID_COMBINATIONS = ["nb", "mk", "dt", "bp", "sz", "nk"]

# Préfixes et suffixes malagasy communs
PREFIXES = [
    "mi",
    "ma",
    "man",
    "mam",
    "maha",
    "mpan",
    "mpam",
    "fi",
    "fan",
    "fam",
    "an",
    "tsi",
]
SUFFIXES = ["ana", "ina", "na", "ka", "tra"]

# ============================================================================
# CHARGEMENT DU DICTIONNAIRE
# ============================================================================


def load_dictionary():
    """
    Charge le dictionnaire depuis les fichiers scrapés ou malagasy_base_data.py
    Priorité: data/malagasy_dictionary.json > malagasy_base_data.py > fallback minimal
    """
    dictionary_file = "data/malagasy_dictionary.json"

    # 1. Essayer de charger depuis le fichier scrapé (priorité)
    try:
        if os.path.exists(dictionary_file):
            print(f"Chargement du dictionnaire depuis {dictionary_file}...")
            with open(dictionary_file, "r", encoding="utf-8") as f:
                loaded_dict = json.load(f)
                print(f"✓ Dictionnaire chargé: {len(loaded_dict):,} mots")
                return set(loaded_dict)
    except Exception as e:
        print(f"⚠ Erreur lecture fichier: {e}")

    # 2. Essayer de charger depuis malagasy_base_data.py
    try:
        from malagasy_base_data import get_base_dictionary

        base_dict = get_base_dictionary()
        print(f"Dictionnaire de base chargé: {len(base_dict):,} mots")
        print(f"Conseil: Lancez 'python3 setup_data.py' pour enrichir")
        return set(base_dict)
    except ImportError:
        print("Fichier malagasy_base_data.py non trouvé")

    # 3. Fallback minimal en dernier recours
    print("Utilisation du dictionnaire minimal de secours")
    minimal_dict = {
        "ny",
        "amin",
        "sy",
        "fa",
        "dia",
        "tsy",
        "ary",
        "koa",
        "vary",
        "sakafo",
        "rano",
        "trano",
        "tanana",
        "ray",
        "reny",
        "tsara",
        "lehibe",
        "kely",
        "mandeha",
        "mihinana",
        "misotro",
        "zanaka",
        "razana",
        "fianakaviana",
        "famadihana",
        "kabary",
        "aho",
        "ianao",
        "izy",
        "isika",
        "omaly",
        "androany",
        "rahampitso",
    }
    print(f"⚠ Dictionnaire minimal: {len(minimal_dict)} mots seulement")
    return minimal_dict


def load_bigram_model():
    """Charge le modèle bigram depuis les fichiers ou malagasy_base_data.py"""
    bigram_file = "data/bigram_model.json"

    # 1. Fichier scrapé (priorité)
    try:
        if os.path.exists(bigram_file):
            print(f"Chargement du modèle N-gram depuis {bigram_file}...")
            with open(bigram_file, "r", encoding="utf-8") as f:
                loaded_model = json.load(f)
                print(f"✓ Modèle N-gram chargé: {len(loaded_model):,} entrées")
                return loaded_model
    except Exception as e:
        print(f"⚠ Erreur N-gram: {e}")

    # 2. malagasy_base_data.py
    try:
        from malagasy_base_data import get_base_bigram_model

        base_bigram = get_base_bigram_model()
        print(f"Modèle N-gram de base: {len(base_bigram):,} entrées")
        return base_bigram
    except ImportError:
        pass

    # 3. Fallback minimal
    return {
        "ny": ["tanana", "vary", "trano", "fianakaviana"],
        "amin": ["ny", "izao", "fotoana"],
        "mandeha": ["any", "aho", "isika"],
        "tsara": ["ny", "loatra", "tokoa"],
    }


def load_word_frequencies():
    """Charge les fréquences de mots"""
    freq_file = "data/word_frequencies.json"

    # 1. Fichier scrapé
    try:
        if os.path.exists(freq_file):
            print(f"Chargement des fréquences depuis {freq_file}...")
            with open(freq_file, "r", encoding="utf-8") as f:
                frequencies = json.load(f)
                print(f"✓ Fréquences chargées: {len(frequencies):,} mots")
                return frequencies
    except:
        pass

    # 2. malagasy_base_data.py
    try:
        from malagasy_base_data import get_base_word_frequencies

        base_freq = get_base_word_frequencies()
        print(f" Fréquences de base: {len(base_freq):,} mots")
        return base_freq
    except ImportError:
        pass

    # 3. Fallback
    return {
        "ny": 1000,
        "amin": 500,
        "sy": 450,
        "fa": 400,
        "dia": 380,
        "tsy": 350,
        "vary": 160,
    }


# Chargement des données au démarrage
print("\n" + "=" * 70)
print(" DÉMARRAGE DE L'API ÉDITEUR MALAGASY INTELLIGENT")
print("=" * 70)

MALAGASY_DICTIONARY = load_dictionary()
BIGRAM_MODEL = load_bigram_model()
WORD_FREQUENCIES = load_word_frequencies()

print("=" * 70 + "\n")

# Table de lemmatisation (racines des mots)
LEMMA_TABLE = {
    "manosika": "tosika",
    "nanosika": "tosika",
    "hanosika": "tosika",
    "manoratra": "soratra",
    "nanoratra": "soratra",
    "hanoratra": "soratra",
    "mandeha": "deha",
    "nandeha": "deha",
    "handeha": "deha",
    "mihinana": "hina",
    "nihinana": "hina",
    "hihinana": "hina",
    "misotro": "sotro",
    "nisotro": "sotro",
    "hisotro": "sotro",
    "mihira": "hira",
    "nihira": "hira",
    "hihira": "hira",
    "matory": "tory",
    "natory": "tory",
    "hatory": "tory",
    "miasa": "asa",
    "niasa": "asa",
    "hiasa": "asa",
}

# Knowledge Graph (Ontologie sémantique)
KNOWLEDGE_GRAPH = {
    "razana": [
        "famadihana",
        "lovantsofina",
        "fomba",
        "tantara",
        "havana",
        "fianakaviana",
    ],
    "famadihana": ["razana", "fomba", "kolontsaina", "fianakaviana", "kabary"],
    "sakafo": ["vary", "laoka", "hanina", "lasopy", "sakay", "hena", "trondro"],
    "vary": ["sakafo", "hanina", "laoka", "masaka", "rano"],
    "fianakaviana": ["ray", "reny", "zanaka", "havana", "razana", "zoky", "zandry"],
    "kabary": ["hira", "ohabolana", "kolontsaina", "fomba", "tantara", "vakiteny"],
    "tanana": ["antananarivo", "antsirabe", "fianarantsoa", "trano", "tanàna"],
    "trano": ["tanana", "efitra", "varavara", "varavarana", "rihana"],
    "ray": ["reny", "zanaka", "fianakaviana", "havana", "ray aman-dreny"],
    "reny": ["ray", "zanaka", "fianakaviana", "havana", "ray aman-dreny"],
    "kolontsaina": [
        "famadihana",
        "kabary",
        "hira",
        "fomba",
        "fombafomba",
        "lovantsofina",
    ],
}

# Mots de sentiment
POSITIVE_WORDS = {
    "tsara",
    "mahafinaritra",
    "soa",
    "sambatra",
    "faly",
    "mahafaly",
    "tsara tarehy",
    "mendrika",
    "mahagaga",
    "matsiro",
    "mahafatifaty",
    "salama",
    "marina",
    "mazava",
    "mamirapiratra",
    "mahatalanjona",
}

NEGATIVE_WORDS = {
    "ratsy",
    "mampalahelo",
    "diso",
    "malahelo",
    "tezitra",
    "mahatsiravina",
    "tsy tsara",
    "mahatsiravina",
    "manjavozavo",
    "mangidy",
    "mafy",
    "diso",
    "diso be",
    "ratsy fanahy",
    "maivana",
}

# Dictionnaire bilingue enrichi (MG <-> FR)
MG_TO_FR = {
    # Famille
    "ray": "père",
    "reny": "mère",
    "zanaka": "enfant",
    "ray aman-dreny": "parents",
    "razana": "ancêtre",
    "zafy": "descendant",
    "havana": "parent/famille",
    "zoky": "aîné",
    "zandry": "cadet",
    "fianakaviana": "famille",
    "vadiko": "mon épouse",
    "vady": "époux/épouse",
    # Nourriture
    "vary": "riz",
    "sakafo": "nourriture/repas",
    "hanina": "nourriture",
    "laoka": "accompagnement",
    "rano": "eau",
    "hena": "viande",
    "trondro": "poisson",
    "mofo": "pain",
    "ronono": "lait",
    "sakay": "piment",
    "lasopy": "soupe",
    "legioma": "légumes",
    # Lieux
    "trano": "maison",
    "tanana": "ville/main",
    "tanàna": "ville",
    "antananarivo": "Antananarivo",
    "antsirabe": "Antsirabe",
    "fianarantsoa": "Fianarantsoa",
    "nosy": "île",
    # Verbes
    "mandeha": "partir/aller",
    "mihinana": "manger",
    "misotro": "boire",
    "matory": "dormir",
    "miasa": "travailler",
    "mihira": "chanter",
    "manoratra": "écrire",
    "mamaky": "lire",
    "miteny": "parler",
    # Adjectifs
    "tsara": "bon/bien",
    "lehibe": "grand",
    "kely": "petit",
    "lava": "long",
    "fohy": "court",
    "mafana": "chaud",
    "mangatsiaka": "froid",
    "fotsy": "blanc",
    "mainty": "noir",
    # Culture
    "famadihana": "retournement des morts",
    "kabary": "discours traditionnel",
    "hira": "chanson",
    "tantara": "histoire",
    "kolontsaina": "culture",
    "ohabolana": "proverbe",
    "lovantsofina": "tradition orale",
    # Temps
    "omaly": "hier",
    "androany": "aujourd'hui",
    "rahampitso": "demain",
    "maraina": "matin",
    "hariva": "soir",
    "alina": "nuit",
    # Mots courants
    "ny": "le/la/les",
    "amin": "à/avec",
    "sy": "et",
    "fa": "mais/car",
    "tsy": "ne...pas",
    "aho": "je/moi",
    "ianao": "tu/toi",
    "izy": "il/elle",
}

# ============================================================================
# MODÈLES PYDANTIC
# ============================================================================


class TextInput(BaseModel):
    text: str


class WordInput(BaseModel):
    word: str


class AutocompleteInput(BaseModel):
    context: str
    limit: int = 5


class TranslationInput(BaseModel):
    word: str
    source_lang: str = "mg"
    target_lang: str = "fr"


# ============================================================================
# FONCTIONS UTILITAIRES NLP
# ============================================================================


def tokenize(text: str) -> List[str]:
    """Tokenisation pour le malagasy"""
    text = text.lower()
    tokens = re.findall(r"\b[a-zàáâèéêìíîòóôùúû-]+\b", text, re.UNICODE)
    return tokens


def contains_invalid_combination(word: str) -> bool:
    """Vérifier les combinaisons phonotactiques invalides"""
    word = word.lower()
    for combo in INVALID_COMBINATIONS:
        if combo in word:
            if combo == "nk" and word.index(combo) > 0:
                continue
            return True
    return False


def find_root(word: str) -> Optional[str]:
    """Lemmatisation: trouver la racine d'un mot"""
    word = word.lower()

    # Table de lemmatisation
    if word in LEMMA_TABLE:
        return LEMMA_TABLE[word]

    # Heuristique: retirer préfixes
    for prefix in PREFIXES:
        if word.startswith(prefix) and len(word) > len(prefix) + 2:
            candidate = word[len(prefix) :]
            if candidate in MALAGASY_DICTIONARY:
                return candidate

    # Heuristique: retirer suffixes
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            candidate = word[: -len(suffix)]
            if candidate in MALAGASY_DICTIONARY:
                return candidate

    return word if word in MALAGASY_DICTIONARY else None


# ============================================================================
# ENDPOINTS API
# ============================================================================


@app.get("/")
async def root():
    return {
        "message": "API Éditeur Malagasy Intelligent",
        "version": "2.0.0",
        "status": "online",
        "dictionary_size": len(MALAGASY_DICTIONARY),
        "endpoints": {
            "spell_check": "/spell-check",
            "autocomplete": "/autocomplete",
            "lemmatize": "/lemmatize",
            "sentiment": "/sentiment",
            "knowledge_graph": "/knowledge-graph",
            "phonotactics": "/validate-phonotactics",
            "translate": "/translate",
            "stats": "/stats",
        },
    }


@app.post("/spell-check")
async def spell_check(input_data: TextInput):
    """
    Correcteur orthographique avec:
    - Dictionnaire malagasy enrichi
    - Distance de Levenshtein
    - Validation phonotactique
    """
    tokens = tokenize(input_data.text)
    results = []

    for token in tokens:
        token_lower = token.lower()

        if token_lower in MALAGASY_DICTIONARY:
            results.append({"word": token, "is_correct": True, "suggestions": []})
        else:
            has_invalid = contains_invalid_combination(token_lower)

            # Suggestions avec rapidfuzz
            suggestions = process.extract(
                token_lower, MALAGASY_DICTIONARY, scorer=fuzz.ratio, limit=5
            )

            filtered_suggestions = [
                {"word": sug[0], "score": sug[1]} for sug in suggestions if sug[1] > 70
            ]

            results.append(
                {
                    "word": token,
                    "is_correct": False,
                    "has_invalid_combination": has_invalid,
                    "suggestions": filtered_suggestions,
                }
            )

    return {
        "original_text": input_data.text,
        "results": results,
        "total_words": len(tokens),
        "errors_found": sum(1 for r in results if not r["is_correct"]),
    }


@app.post("/autocomplete")
async def autocomplete(input_data: AutocompleteInput):
    """Autocomplétion basée sur N-grams"""
    tokens = tokenize(input_data.context)

    if not tokens:
        # Retourner les mots les plus fréquents
        top_words = sorted(WORD_FREQUENCIES.items(), key=lambda x: x[1], reverse=True)
        return {"suggestions": [w[0] for w in top_words[: input_data.limit]]}

    last_word = tokens[-1].lower()

    # Bigram model
    suggestions = []
    if last_word in BIGRAM_MODEL:
        suggestions = BIGRAM_MODEL[last_word][: input_data.limit]

    # Fallback: mots fréquents
    if not suggestions:
        top_words = sorted(WORD_FREQUENCIES.items(), key=lambda x: x[1], reverse=True)
        suggestions = [w[0] for w in top_words[: input_data.limit]]

    return {
        "context": input_data.context,
        "last_word": last_word,
        "suggestions": suggestions,
    }


@app.post("/lemmatize")
async def lemmatize(input_data: WordInput):
    """Lemmatisation malagasy"""
    word = input_data.word.lower()
    root = find_root(word)

    detected_prefixes = [p for p in PREFIXES if word.startswith(p)]
    detected_suffixes = [s for s in SUFFIXES if word.endswith(s)]

    return {
        "original": input_data.word,
        "root": root,
        "prefixes": detected_prefixes,
        "suffixes": detected_suffixes,
        "is_in_dictionary": root in MALAGASY_DICTIONARY if root else False,
    }


@app.post("/sentiment")
async def sentiment_analysis(input_data: TextInput):
    """Analyse de sentiment (Bag of Words)"""
    tokens = tokenize(input_data.text)

    positive_count = sum(1 for token in tokens if token in POSITIVE_WORDS)
    negative_count = sum(1 for token in tokens if token in NEGATIVE_WORDS)

    total_sentiment_words = positive_count + negative_count

    if total_sentiment_words == 0:
        sentiment = "neutre"
        score = 0
    elif positive_count > negative_count:
        sentiment = "positif"
        score = (positive_count - negative_count) / len(tokens)
    elif negative_count > positive_count:
        sentiment = "négatif"
        score = (negative_count - positive_count) / len(tokens)
    else:
        sentiment = "neutre"
        score = 0

    return {
        "text": input_data.text,
        "sentiment": sentiment,
        "score": round(score, 3),
        "positive_words": positive_count,
        "negative_words": negative_count,
        "details": {
            "positive_found": [w for w in tokens if w in POSITIVE_WORDS],
            "negative_found": [w for w in tokens if w in NEGATIVE_WORDS],
        },
    }


@app.post("/knowledge-graph")
async def knowledge_graph_explore(input_data: WordInput):
    """Explorateur sémantique (Knowledge Graph)"""
    word = input_data.word.lower()

    if word in KNOWLEDGE_GRAPH:
        related = KNOWLEDGE_GRAPH[word]

        # Relations de second niveau
        second_level = []
        for related_word in related[:3]:
            if related_word in KNOWLEDGE_GRAPH:
                second_level.extend(KNOWLEDGE_GRAPH[related_word][:2])

        return {
            "word": input_data.word,
            "found": True,
            "direct_relations": related,
            "second_level_relations": list(set(second_level)),
            "semantic_field": (
                "culture" if word in ["razana", "famadihana", "kabary"] else "general"
            ),
        }
    else:
        similar = process.extract(word, KNOWLEDGE_GRAPH.keys(), limit=3)
        return {
            "word": input_data.word,
            "found": False,
            "similar_concepts": [s[0] for s in similar if s[1] > 70],
        }


@app.post("/validate-phonotactics")
async def validate_phonotactics(input_data: WordInput):
    """Validation phonotactique"""
    word = input_data.word.lower()
    has_invalid = contains_invalid_combination(word)

    invalid_found = []
    for combo in INVALID_COMBINATIONS:
        if combo in word:
            pos = word.index(combo)
            if combo == "nk" and pos > 0:
                continue
            invalid_found.append({"combination": combo, "position": pos})

    return {
        "word": input_data.word,
        "is_valid": not has_invalid,
        "invalid_combinations": invalid_found,
        "message": (
            "Règles phonotactiques respectées"
            if not has_invalid
            else "Combinaisons invalides détectées"
        ),
    }


@app.post("/translate")
async def translate_word(input_data: TranslationInput):
    """Traduction mot-à-mot MG <-> FR"""
    word = input_data.word.lower()

    if input_data.source_lang == "mg" and input_data.target_lang == "fr":
        translation = MG_TO_FR.get(word)

        if not translation:
            similar = process.extractOne(word, MG_TO_FR.keys())
            return {
                "word": input_data.word,
                "translation": None,
                "found": False,
                "suggestion": (
                    {
                        "word": similar[0],
                        "translation": MG_TO_FR[similar[0]],
                        "similarity": similar[1],
                    }
                    if similar and similar[1] > 70
                    else None
                ),
            }

        return {
            "word": input_data.word,
            "translation": translation,
            "found": True,
            "source_lang": "mg",
            "target_lang": "fr",
        }

    return {"error": "Direction de traduction non supportée"}


@app.get("/stats")
async def get_statistics():
    """Statistiques du système"""
    dict_size = len(MALAGASY_DICTIONARY)
    data_source = (
        "scraped" if dict_size > 500 else "base" if dict_size > 100 else "minimal"
    )

    return {
        "dictionary_size": dict_size,
        "bigram_entries": len(BIGRAM_MODEL),
        "word_frequencies_loaded": len(WORD_FREQUENCIES),
        "knowledge_graph_nodes": len(KNOWLEDGE_GRAPH),
        "lemma_rules": len(LEMMA_TABLE),
        "prefixes": len(PREFIXES),
        "suffixes": len(SUFFIXES),
        "positive_words": len(POSITIVE_WORDS),
        "negative_words": len(NEGATIVE_WORDS),
        "translation_pairs": len(MG_TO_FR),
        "data_source": data_source,
        "status": {
            "scraped_data": dict_size > 500,
            "base_data": 100 < dict_size <= 500,
            "minimal_data": dict_size <= 100,
        },
        "recommendations": {
            "scraping": (
                "Lancez 'python3 setup_data.py --force --all-sources'"
                if dict_size < 1000
                else "Données enrichies ✓"
            ),
            "base_data": (
                "Fichier malagasy_base_data.py chargé"
                if 100 < dict_size <= 500
                else None
            ),
        },
    }


# ============================================================================
# LANCEMENT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("\n Lancement du serveur...")
    print("URL: http://localhost:8000")
    print("=" * 70 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
