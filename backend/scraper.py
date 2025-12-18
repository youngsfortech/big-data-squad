"""
Script de Scraping pour enrichir le dictionnaire Malagasy
Sources: Wikipedia MG, Teny Malagasy, Rakibolana, Wiktionary MG

Installation: pip install beautifulsoup4 requests
Usage: python3 scraper.py
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from collections import Counter
import time
import os
import urllib3

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MalagasyScraper:
    def __init__(self):
        self.dictionary = set()
        self.word_frequencies = Counter()
        self.corpus_text = []
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )

    def scrape_wikipedia_mg(self, num_articles=50):
        """
        Scraper les articles Wikipedia Malagasy
        """
        print(f"Scraping {num_articles} articles de Wikipedia MG...")

        base_url = "https://mg.wikipedia.org/w/api.php"

        # Paramètres pour obtenir des articles aléatoires
        params = {
            "action": "query",
            "format": "json",
            "list": "random",
            "rnnamespace": 0,
            "rnlimit": min(num_articles, 50),
        }

        try:
            response = self.session.get(
                base_url, params=params, timeout=15, verify=False
            )
            response.raise_for_status()

            data = response.json()
            articles = data.get("query", {}).get("random", [])
            print(f"   Trouvé {len(articles)} articles")

            for idx, article in enumerate(articles):
                title = article["title"]
                page_id = article["id"]

                content = self._get_article_content(page_id)
                if content:
                    self.corpus_text.append(content)
                    words = self._tokenize(content)
                    self.dictionary.update(words)
                    self.word_frequencies.update(words)

                if (idx + 1) % 10 == 0:
                    print(f"   Traité: {idx + 1}/{len(articles)} articles")

                time.sleep(0.2)

            print(f"✓ Wikipedia MG: {len(self.dictionary)} mots collectés")

        except Exception as e:
            print(f"Erreur Wikipedia: {e}")
            print("   Tentative de scraping direct des pages...")
            self._scrape_wikipedia_direct()

    def _scrape_wikipedia_direct(self):
        """Scraper directement les pages HTML de Wikipedia"""
        try:
            # Liste de pages populaires en malagasy
            pages = [
                "Madagasikara",
                "Antananarivo",
                "Firenena",
                "Tantara",
                "Siansa",
                "Matematika",
                "Fizika",
                "Biolojia",
                "Toekarena",
                "Kolontsaina",
                "Literatiora",
                "Mozika",
                "Kanto",
                "Fanatanjahantena",
            ]

            for page in pages:
                url = f"https://mg.wikipedia.org/wiki/{page}"
                try:
                    response = self.session.get(url, timeout=10, verify=False)
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Extraire le contenu principal
                    content_div = soup.find("div", {"id": "mw-content-text"})
                    if content_div:
                        text = content_div.get_text()
                        self.corpus_text.append(text)
                        words = self._tokenize(text)
                        self.dictionary.update(words)
                        self.word_frequencies.update(words)

                    time.sleep(0.5)
                except:
                    continue

            print(f"✓ Scraping direct: {len(self.dictionary)} mots collectés")
        except Exception as e:
            print(f"⚠ Erreur scraping direct: {e}")

    def _get_article_content(self, page_id):
        """Récupérer le contenu d'un article Wikipedia"""
        url = "https://mg.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "pageids": page_id,
            "prop": "extracts",
            "explaintext": True,
        }

        try:
            response = self.session.get(url, params=params, timeout=10, verify=False)
            data = response.json()
            pages = data.get("query", {}).get("pages", {})

            if str(page_id) in pages:
                extract = pages[str(page_id)].get("extract", "")
                return extract
        except:
            pass

        return None

    def scrape_teny_malagasy(self):
        """
        Scraper le dictionnaire Teny Malagasy avec gestion SSL
        """
        print("Scraping Teny Malagasy (dictionnaire)...")

        base_url = "https://tenymalagasy.org"
        words_added = 0

        try:
            # Essayer avec verify=False pour SSL
            response = self.session.get(base_url, timeout=15, verify=False)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.content, "html.parser")

            # Extraire tous les textes de la page
            all_text = soup.get_text()
            words = self._tokenize(all_text)
            initial_count = len(self.dictionary)
            self.dictionary.update(words)
            words_added = len(self.dictionary) - initial_count

            # Chercher des liens
            links = soup.find_all("a", href=True)
            for link in links[:100]:  # Limiter à 100 liens
                text = link.get_text(strip=True).lower()
                if text and self._is_valid_malagasy_word(text):
                    self.dictionary.add(text)
                    words_added += 1

            print(f"✓ Teny Malagasy: {words_added} mots ajoutés")

        except Exception as e:
            print(f"⚠ Erreur Teny Malagasy: {e}")
            print("   Utilisation d'un dictionnaire de base...")
            self._load_base_dictionary()

    def _load_base_dictionary(self):
        """Charger un dictionnaire de base de mots malagasy courants"""
        try:
            from malagasy_base_data import get_base_dictionary

            base_words = get_base_dictionary()
            self.dictionary.update(base_words)
            print(f"   ✓ Base dictionary: {len(base_words)} mots ajoutés")
        except ImportError:
            print("   ⚠ Fichier malagasy_base_data.py non trouvé")
            # Fallback minimal
            minimal_words = [
                "ny",
                "amin",
                "sy",
                "fa",
                "dia",
                "tsy",
                "ary",
                "vary",
                "sakafo",
                "rano",
                "trano",
                "tanana",
            ]
            self.dictionary.update(minimal_words)
            print(f"   ✓ Dictionnaire minimal: {len(minimal_words)} mots")

    def scrape_rakibolana(self):
        """
        Scraper rakibolana.org
        """
        print("Scraping Rakibolana...")

        base_url = "https://rakibolana.org"
        words_added = 0

        try:
            response = self.session.get(base_url, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, "html.parser")

            # Extraire tous les mots
            all_text = soup.get_text()
            words = self._tokenize(all_text)
            initial_count = len(self.dictionary)
            self.dictionary.update(words)
            words_added = len(self.dictionary) - initial_count

            print(f"✓ Rakibolana: {words_added} mots ajoutés")

        except Exception as e:
            print(f"⚠ Erreur Rakibolana: {e}")

    def scrape_wiktionary_mg(self, num_pages=100):
        """
        Scraper Wiktionary Malagasy
        """
        print(f"Scraping Wiktionary MG...")

        base_url = "https://mg.wiktionary.org/w/api.php"
        words_added = 0

        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "allpages",
                "aplimit": num_pages,
            }

            response = self.session.get(
                base_url, params=params, timeout=15, verify=False
            )
            response.raise_for_status()
            data = response.json()

            pages = data.get("query", {}).get("allpages", [])

            for page in pages:
                title = page["title"].lower()
                if self._is_valid_malagasy_word(title):
                    self.dictionary.add(title)
                    words_added += 1

            print(f"✓ Wiktionary MG: {words_added} mots ajoutés")

        except Exception as e:
            print(f"⚠ Erreur Wiktionary MG: {e}")
            # Scraping direct comme fallback
            self._scrape_wiktionary_direct()

    def _scrape_wiktionary_direct(self):
        """Scraper directement les pages du Wiktionary"""
        try:
            url = "https://mg.wiktionary.org/wiki/Fandraisana"
            response = self.session.get(url, timeout=10, verify=False)
            soup = BeautifulSoup(response.content, "html.parser")

            text = soup.get_text()
            words = self._tokenize(text)
            self.dictionary.update(words)
            print(f"   Wiktionary direct: {len(words)} mots ajoutés")
        except:
            pass

    def _tokenize(self, text):
        """Tokenisation pour le malagasy"""
        text = text.lower()
        text = re.sub(r"[^\w\s-]", " ", text)
        words = re.findall(r"\b[a-zàáâèéêìíîòóôùúû-]{2,}\b", text, re.UNICODE)
        valid_words = [w for w in words if self._is_valid_malagasy_word(w)]
        return valid_words

    def _is_valid_malagasy_word(self, word):
        """Vérifier si un mot est malagasy"""
        if len(word) < 2 or len(word) > 30:
            return False

        # Mots à éviter
        stop_words = [
            "http",
            "https",
            "www",
            "com",
            "org",
            "html",
            "php",
            "css",
            "jpg",
            "png",
        ]
        if word in stop_words:
            return False

        # Combinaisons interdites en malagasy
        invalid_combos = ["nb", "mk", "dt", "bp", "sz", "qq", "xx"]
        for combo in invalid_combos:
            if combo in word:
                return False

        if not re.match(r"^[a-zàáâèéêìíîòóôùúû-]+$", word, re.UNICODE):
            return False

        return True

    def build_bigram_model(self):
        """Construire un modèle bigram"""
        print("Construction du modèle N-gram...")

        bigram_model = {}

        for text in self.corpus_text:
            words = self._tokenize(text)

            for i in range(len(words) - 1):
                word1, word2 = words[i], words[i + 1]

                if word1 not in bigram_model:
                    bigram_model[word1] = Counter()

                bigram_model[word1][word2] += 1

        final_model = {}
        for word, counter in bigram_model.items():
            final_model[word] = [w for w, _ in counter.most_common(10)]

        print(f"   Modèle bigram: {len(final_model)} entrées")
        return final_model

    def export_data(self, output_dir="data"):
        """Exporter les données"""
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n Export des données vers {output_dir}/...")

        # Dictionnaire
        dict_file = os.path.join(output_dir, "malagasy_dictionary.json")
        with open(dict_file, "w", encoding="utf-8") as f:
            json.dump(sorted(list(self.dictionary)), f, ensure_ascii=False, indent=2)
        print(f"   ✓ {dict_file} ({len(self.dictionary)} mots)")

        # Fréquences
        freq_file = os.path.join(output_dir, "word_frequencies.json")
        top_words = dict(self.word_frequencies.most_common(1000))
        with open(freq_file, "w", encoding="utf-8") as f:
            json.dump(top_words, f, ensure_ascii=False, indent=2)
        print(f"   ✓ {freq_file} (top 1000)")

        # Modèle bigram
        bigram_model = self.build_bigram_model()
        bigram_file = os.path.join(output_dir, "bigram_model.json")
        with open(bigram_file, "w", encoding="utf-8") as f:
            json.dump(bigram_model, f, ensure_ascii=False, indent=2)
        print(f"   ✓ {bigram_file}")

        # Corpus
        corpus_file = os.path.join(output_dir, "corpus_sample.txt")
        with open(corpus_file, "w", encoding="utf-8") as f:
            sample = "\n\n".join(self.corpus_text[:50])
            f.write(sample)
        print(f"   ✓ {corpus_file}")

        print(f"\n Statistiques finales:")
        print(f"   • Mots uniques: {len(self.dictionary)}")
        print(f"   • Articles traités: {len(self.corpus_text)}")
        print(f"   • Mots totaux: {sum(self.word_frequencies.values())}")

    def get_statistics(self):
        """Afficher les statistiques"""
        print("\n" + "=" * 60)
        print("STATISTIQUES DU SCRAPING")
        print("=" * 60)
        print(f"Mots uniques: {len(self.dictionary)}")
        print(f"Articles traités: {len(self.corpus_text)}")
        print(f"Mots totaux: {sum(self.word_frequencies.values())}")

        if self.word_frequencies:
            print("\n Top 20 mots les plus fréquents:")
            for word, count in self.word_frequencies.most_common(20):
                print(f"   {word:20s} : {count:>5d}")
        print("=" * 60)


def main():
    """Script principal"""
    print("=" * 60)
    print("SCRAPER CORPUS MALAGASY (Version Corrigée)")
    print("=" * 60)
    print()

    scraper = MalagasyScraper()

    # 1. Wikipedia MG
    scraper.scrape_wikipedia_mg(num_articles=50)
    print()

    # 2. Teny Malagasy
    scraper.scrape_teny_malagasy()
    print()

    # 3. Rakibolana
    scraper.scrape_rakibolana()
    print()

    # 4. Wiktionary MG
    scraper.scrape_wiktionary_mg()
    print()

    # 5. Statistiques
    scraper.get_statistics()

    # 6. Export
    scraper.export_data()

    print("\n" + "=" * 60)
    print("SCRAPING TERMINÉ!")
    print("=" * 60)
    print("Fichiers dans 'data/':")
    print("   • malagasy_dictionary.json")
    print("   • word_frequencies.json")
    print("   • bigram_model.json")
    print("   • corpus_sample.txt")
    print("=" * 60)


if __name__ == "__main__":
    main()
