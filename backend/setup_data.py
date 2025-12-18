"""
Script d'Initialisation Automatique des Données
Lance automatiquement le scraping si les données n'existent pas

Usage:
    python3 setup_data.py                   # Setup interactif
    python3 setup_data.py --force           # Force le re-scraping
    python3 setup_data.py --quick           # Scraping rapide (50 articles)
    python3 setup_data.py --all-sources     # Active toutes les sources
    python3 setup_data.py --minimal         # Données minimales uniquement
"""

import os
import sys
import json


def check_data_exists():
    """Vérifie si les fichiers de données existent"""
    required_files = [
        "data/malagasy_dictionary.json",
        "data/bigram_model.json",
        "data/word_frequencies.json",
    ]

    return all(os.path.exists(f) for f in required_files)


def get_data_stats():
    """Récupère les statistiques des données existantes"""
    try:
        with open("data/malagasy_dictionary.json", "r", encoding="utf-8") as f:
            dictionary = json.load(f)

        with open("data/bigram_model.json", "r", encoding="utf-8") as f:
            bigram = json.load(f)

        with open("data/word_frequencies.json", "r", encoding="utf-8") as f:
            frequencies = json.load(f)

        return {
            "dictionary_words": len(dictionary),
            "bigram_entries": len(bigram),
            "word_frequencies": len(frequencies),
        }
    except:
        return None


def run_scraper(num_articles=50, all_sources=False):
    """Lance le scraper avec les options spécifiées"""
    print("\n" + "=" * 70)
    print("LANCEMENT DU SCRAPING")
    print("=" * 70)

    try:
        # Import dynamique du scraper
        try:
            from scraper import MalagasyScraper
        except ImportError:
            print("\n ERREUR: Le module 'scraper.py' n'est pas disponible")
            print("   Assurez-vous que scraper.py est dans le même dossier")
            return False

        scraper = MalagasyScraper()

        print(f"\n Configuration du scraping:")
        print(f"   • Articles Wikipedia: {num_articles}")
        print(f"   • Toutes les sources: {'Oui' if all_sources else 'Non'}")
        print(f"\n Temps estimé: 2-5 minutes selon votre connexion...")
        print()

        # 1. Wikipedia MG (toujours activé)
        scraper.scrape_wikipedia_mg(num_articles=num_articles)
        print()

        # 2. Teny Malagasy (toujours activé)
        scraper.scrape_teny_malagasy()
        print()

        # 3. Sources additionnelles (si demandé)
        if all_sources:
            scraper.scrape_rakibolana()
            print()

            scraper.scrape_wiktionary_mg()
            print()
        else:
            print("  Sources additionnelles désactivées")
            print("   Pour les activer: python3 setup_data.py --all-sources")
            print()

        # 4. Statistiques
        scraper.get_statistics()

        # 5. Export des données
        print("\n Export des données...")
        scraper.export_data()

        print("\n" + "=" * 70)
        print(" SCRAPING TERMINÉ AVEC SUCCÈS!")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"\n ERREUR lors du scraping: {e}")
        import traceback

        traceback.print_exc()
        return False


def create_minimal_data():
    """Crée des fichiers de données minimaux si le scraping échoue"""
    print("\n Création de données minimales de secours...")

    os.makedirs("data", exist_ok=True)

    try:
        # Importer les données de base depuis le fichier centralisé
        from malagasy_base_data import (
            get_base_dictionary,
            get_base_bigram_model,
            get_base_word_frequencies,
            get_base_corpus_sample,
        )

        minimal_dict = get_base_dictionary()
        minimal_bigram = get_base_bigram_model()
        minimal_freq = get_base_word_frequencies()
        corpus_sample = get_base_corpus_sample()

    except ImportError:
        print("  Fichier malagasy_base_data.py non trouvé")
        print("   Utilisation de données minimales de secours...")

        # Fallback minimal si le fichier n'existe pas
        minimal_dict = [
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
        ]

        minimal_bigram = {
            "ny": ["tanana", "vary", "trano"],
            "amin": ["ny", "izao"],
            "mandeha": ["any", "aho"],
        }

        minimal_freq = {"ny": 100, "amin": 50, "sy": 45, "fa": 40, "dia": 38}

        corpus_sample = "Madagasikara dia firenena lehibe."

    # Sauvegarder les fichiers
    with open("data/malagasy_dictionary.json", "w", encoding="utf-8") as f:
        json.dump(sorted(minimal_dict), f, ensure_ascii=False, indent=2)

    with open("data/bigram_model.json", "w", encoding="utf-8") as f:
        json.dump(minimal_bigram, f, ensure_ascii=False, indent=2)

    with open("data/word_frequencies.json", "w", encoding="utf-8") as f:
        json.dump(minimal_freq, f, ensure_ascii=False, indent=2)

    with open("data/corpus_sample.txt", "w", encoding="utf-8") as f:
        f.write(corpus_sample)

    print(f" Fichiers minimaux créés:")
    print(f"   • Dictionnaire: {len(minimal_dict)} mots")
    print(f"   • Modèle N-gram: {len(minimal_bigram)} entrées")
    print(f"   • Fréquences: {len(minimal_freq)} mots")
    print(f"   • Corpus: échantillon de texte")


def main():
    """Fonction principale"""
    print("\n" + "=" * 70)
    print(" SETUP DONNÉES - ÉDITEUR MALAGASY INTELLIGENT")
    print("=" * 70)

    # Analyser les arguments
    force_scraping = "--force" in sys.argv
    quick_mode = "--quick" in sys.argv
    all_sources = "--all-sources" in sys.argv
    minimal_only = "--minimal" in sys.argv

    # Créer le dossier data
    os.makedirs("data", exist_ok=True)

    # Vérifier si les données existent
    data_exists = check_data_exists()

    if data_exists and not force_scraping:
        print("\n Les fichiers de données existent déjà!")
        stats = get_data_stats()
        if stats:
            print(f"\n Statistiques actuelles:")
            print(f"   • Dictionnaire: {stats['dictionary_words']:,} mots")
            print(f"   • Modèle N-gram: {stats['bigram_entries']:,} entrées")
            print(f"   • Fréquences: {stats['word_frequencies']:,} mots")

        print(f"\n Options disponibles:")
        print(f"   • python3 setup_data.py --force         # Re-scraping complet")
        print(
            f"   • python3 setup_data.py --quick         # Scraping rapide (50 articles)"
        )
        print(f"   • python3 setup_data.py --all-sources   # Toutes les sources")
        print(
            f"   • python3 setup_data.py --minimal       # Données minimales uniquement"
        )

        print(f"\n Vous pouvez maintenant lancer le serveur:")
        print(f"   uvicorn main:app --reload")
        return

    # Mode minimal uniquement
    if minimal_only:
        print("\n Mode minimal activé")
        create_minimal_data()
        print(f"\n Setup terminé!")
        return

    # Décider du nombre d'articles
    num_articles = 50 if quick_mode else 50  # Par défaut 50

    if force_scraping:
        print("\n Mode FORCE activé: Re-scraping des données...")
    else:
        print("\n Aucune donnée trouvée. Initialisation nécessaire...")

    print(f"\n Options de setup:")
    print(f"   1. Scraping automatique (recommandé)")
    print(f"   2. Données minimales seulement (pour test rapide)")
    print(f"   3. Annuler")

    # En mode automatique, lancer directement
    if force_scraping or quick_mode or all_sources:
        choice = "1"
    else:
        try:
            choice = input("\n Votre choix (1/2/3): ").strip()
        except (EOFError, KeyboardInterrupt):
            choice = "2"  # Fallback pour environnements sans input

    if choice == "1":
        print(f"\n Lancement du scraping automatique...")

        success = run_scraper(num_articles=num_articles, all_sources=all_sources)

        if not success:
            print(f"\n  Scraping échoué. Création de données minimales...")
            create_minimal_data()

    elif choice == "2":
        create_minimal_data()

    else:
        print(f"\n Setup annulé.")
        print(f"   L'application utilisera des données par défaut.")
        return

    print("\n" + "=" * 70)
    print(" SETUP TERMINÉ!")
    print("=" * 70)
    print(f"\n Prochaines étapes:")
    print(f"   1. Vérifier les fichiers dans data/")
    print(f"   2. Lancer le serveur: uvicorn main:app --reload")
    print(f"   3. Ouvrir http://localhost:8000")
    print(f"\n Documentation: README.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
