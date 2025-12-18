"""

Données de base pour le dictionnaire Malagasy
Ce fichier contient les mots, bigrams et fréquences minimales

"""

# Dictionnaire de base - Mots malagasy courants
BASE_DICTIONARY = [
    # Pronoms et mots de base
    'aho', 'ianao', 'izy', 'isika', 'izahay', 'ianareo', 'izy ireo',
    'ny', 'amin', 'sy', 'na', 'fa', 'raha', 'dia', 'ary', 'koa', 'tsy', 'eny', 'tsia',
    
    # Famille
    'ray', 'reny', 'zanaka', 'rahalahy', 'anabavy', 'rahavavy', 'razana', 'zafy', 'havana',
    'vadiko', 'vady', 'zoky', 'zandry', 'fianakaviana', 'olona',
    
    # Nourriture
    'vary', 'sakafo', 'hanina', 'laoka', 'rano', 'hena', 'trondro',
    'lasopy', 'sakay', 'mofo', 'ronono', 'legioma', 'voankazo',
    'kafe', 'dite', 'divay', 'toaka',
    
    # Verbes d'action
    'mandeha', 'mipetraka', 'mihira', 'mihinana', 'misotro', 'matory', 'miasa',
    'manoratra', 'mamaky', 'miteny', 'miresaka', 'manome', 'mandray',
    'mamita', 'manosika', 'misintona', 'manokatra', 'manidy',
    'mivoaka', 'miditra', 'miakatra', 'midina', 'mihazakazaka',
    'manao', 'milaza', 'manontany', 'mamaly', 'mianatra', 'mampianatra', 'milalao',
    'mifoha', 'matory',
    
    # Verbes d'état
    'misy', 'tsy misy', 'mety', 'tsy mety', 'mahita', 'tsy mahita',
    'mahalala', 'tsy mahalala', 'mahay', 'tsy mahay', 'afaka', 'tsy afaka',
    
    # Adjectifs
    'tsara', 'ratsy', 'lehibe', 'kely', 'lava', 'fohy',
    'mafana', 'mangatsiaka', 'fotsy', 'mainty', 'mena', 'manga', 'maitso',
    'mavomavo', 'matsiro', 'mangidy', 'mamy', 'mavo',
    'be', 'vitsy', 'betsaka', 'madinika', 'goavana',
    'marina', 'diso', 'mazava', 'maizina',
    'volomboasary', 'volontany',
    
    # Lieux
    'trano', 'tanana', 'tanàna', 'nosy', 'morontsiraka', 'efitra',
    'antananarivo', 'antsirabe', 'fianarantsoa', 'toamasina', 'mahajanga', 'toliara',
    'ambohimanga', 'andasibe', 'isalo', 'firenena', 'tany', 'lanitra',
    
    # Temps
    'omaly', 'androany', 'rahampitso', 'maraina', 'tolakandro', 'hariva', 'alina',
    'ora', 'minitra', 'segondra', 'andro', 'herinandro', 'volana', 'taona',
    'fotoana', 'fahizay', 'ankehitriny', 'ho avy',
    
    # Nombres
    'iray', 'roa', 'telo', 'efatra', 'dimy', 'enina', 'fito', 'valo', 'sivy', 'folo',
    'roapolo', 'telopolo', 'efapolo', 'dimampolo', 'zato', 'arivo', 'alina',
    
    # Culture malagasy
    'famadihana', 'kabary', 'hira', 'tantara', 'kolontsaina',
    'vakoka', 'mozika', 'fomba', 'fanao', 'fombafomba',
    'lovantsofina', 'ohabolana', 'vakiteny', 'angano',
    
    # Questions
    'inona', 'aiza', 'oviana', 'ahoana', 'nahoana', 'firy', 'iza',
    'manao ahoana', 'inona vaovao',
    
    # Expressions courantes
    'azafady', 'misaotra', 'veloma', 'manahoana', 'salama',
    'tsara fa tsy mahay', 'marina tokoa', 'tsy maninona',
    'tena', 'tokoa', 'mihitsy', 'loatra', 'be dia be',
    
    # Nature
    'ala', 'voromahery', 'biby', 'zavamaniry', 'hazo', 'voniny',
    'masoandro', 'kintana', 'rahona', 'orana',
    'rivotra', 'varatra', 'vato', 'fasika',
    
    # Corps humain
    'loha', 'maso', 'orona', 'vava', 'sofina', 'tanana', 'tongotra',
    'fo', 'aina', 'vatana', 'hoditra',
    
    # Lieux publics et services
    'fiangonana', 'sekoly', 'hopitaly', 'tsena', 'magazay',
    
    # Argent et commerce
    'vola', 'ariary', 'vidiny', 'lafo', 'mora',
    'mankasitraka', 'mirary', 'mangataka', 'manome vola',
    
    # Mots de liaison
    'nefa', 'kanefa', 'saingy', 'rehefa', 'satria', 'noho', 'ho', 'eo', 'ao',
    'izany', 'izao', 'io', 'ity', 'ireo', 'ireny', 'ilay',
    'ka', 'mba', 'anefa', 'ary', 'fa',
]

# Modèle Bigram de base
BASE_BIGRAM_MODEL = {
    'ny': ['tanana', 'fianakaviana', 'sakafo', 'razana', 'trano', 'firenena', 'olona'],
    'amin': ['ny', 'izao', 'fotoana', 'alahady', 'androany', 'ity'],
    'mandeha': ['any', 'mankany', 'mody', 'miasa', 'mianatra', 'aho'],
    'mihinana': ['vary', 'sakafo', 'laoka', 'mofo', 'hena'],
    'misotro': ['rano', 'kafe', 'dite', 'ronono'],
    'tsara': ['ny', 'izany', 'loatra', 'tokoa', 'be'],
    'lehibe': ['ny', 'ilay', 'loatra', 'be', 'izy'],
    'trano': ['lehibe', 'kely', 'ny', 'vaovao', 'tsara'],
    'fianakaviana': ['malagasy', 'lehibe', 'ny', 'tsara', 'be'],
    'ray': ['aman', 'dreny', 'sy', 'be', 'aman-dreny'],
    'manao': ['ahoana', 'izany', 'azy', 'izao', 'ny'],
    'tsy': ['misy', 'mety', 'afaka', 'maninona', 'mahay', 'tsara'],
    'dia': ['mandeha', 'misy', 'tsara', 'izany', 'ny'],
    'fa': ['tsara', 'ratsy', 'lehibe', 'marina', 'tsy'],
    'vary': ['sy', 'laoka', 'amin', 'ny', 'misy'],
    'aho': ['dia', 'mandeha', 'misy', 'tsy', 'koa'],
    'ianao': ['dia', 've', 'koa', 'manao', 'ahoana'],
    'izy': ['dia', 'koa', 'ireo', 'manao', 'misy'],
    'matory': ['aho', 'izy', 'ianao', 'isika', 'ny'],
    'sakafo': ['malagasy', 'tsara', 'matsiro', 'ny', 'be'],
}

# Fréquences de mots de base
BASE_WORD_FREQUENCIES = {
    'ny': 1000,
    'amin': 500,
    'sy': 450,
    'fa': 400,
    'dia': 380,
    'tsy': 350,
    'ary': 320,
    'koa': 300,
    'raha': 280,
    'na': 260,
    'tsara': 250,
    'lehibe': 200,
    'izy': 190,
    'aho': 180,
    'ianao': 170,
    'vary': 160,
    'trano': 150,
    'mandeha': 140,
    'mihinana': 130,
    'razana': 120,
    'sakafo': 110,
    'rano': 100,
    'ray': 95,
    'reny': 90,
    'zanaka': 85,
    'manao': 80,
    'misy': 75,
    'tanana': 70,
    'olona': 65,
    'izany': 60,
    'izao': 55,
}

# Corpus sample minimal
BASE_CORPUS_SAMPLE = """Madagasikara dia firenena lehibe any Afrikandrefana.
Ny renivohitra dia Antananarivo.
Ny olona malagasy dia manana kolontsaina manan-danja.
Ny vary dia sakafo fototra eto Madagasikara.
Ny famadihana dia fomba fanao malagasy malaza.

Ny ray aman-dreny malagasy dia tena manaja ny razana.
Ny zanaka dia mianatra ny fomba malagasy.
Ny trano malagasy dia mahitsy sy tsara tarehy.

Eto Madagasikara dia misy biby tsy hita any amin'ny tany hafa.
Ny ala tropikaly dia be eto amin'ny nosy.
Ny kolontsaina malagasy dia mampifangaro ny fomba afrikanina sy aziatika.

Ny kabary dia teny feno hevi-lalina.
Ny hira gasy dia maneho ny fihetseham-pon'ny olona malagasy.
Ny ohabolana dia mampita ny fahendrena malagasy.
"""

def get_base_dictionary():
    """Retourne le dictionnaire de base"""
    return BASE_DICTIONARY.copy()

def get_base_bigram_model():
    """Retourne le modèle bigram de base"""
    return BASE_BIGRAM_MODEL.copy()

def get_base_word_frequencies():
    """Retourne les fréquences de base"""
    return BASE_WORD_FREQUENCIES.copy()

def get_base_corpus_sample():
    """Retourne le corpus sample de base"""
    return BASE_CORPUS_SAMPLE