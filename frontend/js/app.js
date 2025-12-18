const { useState } = React;

// Récupération des modules
const {
  CheckIcon,
  SentimentIcon,
  DocumentIcon,
  BookIcon,
  DeleteIcon,
  ChartIcon,
  TranslateIcon,
  LinkIcon,
  SoundIcon,
  HappyIcon,
  SadIcon,
  NeutralIcon,
} = window.Icons;

const {
  spellCheck,
  analyzeSentiment: analyzeSentimentAPI,
  lemmatizeWord,
  getKnowledgeGraph,
  translateWord,
  validatePhonotactics,
} = window.ApiService;

const { updateStats, calculateAccuracy, getSampleText } = window.Utils;
const useQuillEditor = window.useQuillEditor;

window.MalagasyEditor = function() {
  const [text, setText] = useState("");
  const [spellCheckResults, setSpellCheckResults] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [knowledgeGraph, setKnowledgeGraph] = useState(null);
  const [lemma, setLemma] = useState(null);
  const [translation, setTranslation] = useState(null);
  const [phonotactics, setPhonotactics] = useState(null);
  const [stats, setStats] = useState({ words: 0, chars: 0, errors: 0 });
  const [activeTab, setActiveTab] = useState("spell");
  const [loading, setLoading] = useState(false);
  const [selectedWord, setSelectedWord] = useState("");

  const handleTextChange = (content) => {
    setText(content);
    setStats(updateStats(content, spellCheckResults));
  };

  const handleTextSelection = (word) => {
    setSelectedWord(word);
    setActiveTab("word")
    analyzeWord(word);
  };

  const quillRef = useQuillEditor(handleTextChange, handleTextSelection);

  const analyzeWord = async (word) => {
    try {
      const [lemmaData, kgData, transData, phonoData] = await Promise.all([
        lemmatizeWord(word),
        getKnowledgeGraph(word),
        translateWord(word, "mg", "fr"),
        validatePhonotactics(word),
      ]);

      setLemma(lemmaData);
      setKnowledgeGraph(kgData);
      setTranslation(transData);
      setPhonotactics(phonoData);
    } catch (error) {
      console.error("Error analyzing word:", error);
    }
  };

  const performSpellCheck = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setActiveTab("spell");

    try {
      const data = await spellCheck(text);
      setSpellCheckResults(data);
      setStats(updateStats(text, data));
    } catch (error) {
      console.error("Spell check error:", error);
      alert("Erreur de connexion au serveur. Vérifiez que le backend est lancé.");
    } finally {
      setLoading(false);
    }
  };

  const analyzeSentiment = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setActiveTab("sentiment");

    try {
      const data = await analyzeSentimentAPI(text);
      setSentiment(data);
    } catch (error) {
      console.error("Sentiment analysis error:", error);
    } finally {
      setLoading(false);
    }
  };

  const replaceWord = (oldWord, newWord) => {
    const content = quillRef.current.getText();
    const newContent = content.replace(
      new RegExp(`\\b${oldWord}\\b`, "gi"),
      newWord
    );
    quillRef.current.setText(newContent);
  };

  const insertSampleText = () => {
    const sample = getSampleText();
    quillRef.current.setText(sample);
    setText(sample);
  };

  const getSentimentIcon = (sentiment) => {
    if (sentiment === "positif") return <HappyIcon />;
    if (sentiment === "négatif") return <SadIcon />;
    return <NeutralIcon />;
  };

  const accuracy = calculateAccuracy(stats);

  return (
    <div className="app-container">
      <header className="modern-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">MG</div>
            <div className="header-text">
              <h1>Éditeur Malagasy Intelligent</h1>
              <p>Éditeur de texte augmenté par l'IA - ISPM</p>
            </div>
          </div>
          <div className="header-stats">
            <div className="quick-stat">
              <div className="quick-stat-value">{stats.words}</div>
              <div className="quick-stat-label">Mots</div>
            </div>
            <div className="quick-stat">
              <div className="quick-stat-value">{accuracy}%</div>
              <div className="quick-stat-label">Précision</div>
            </div>
          </div>
        </div>
      </header>

      <div className="main-content">
        <div className="editor-card">
          <div className="editor-toolbar">
            <button
              className="action-btn primary"
              onClick={performSpellCheck}
              disabled={loading}
            >
              {loading ? <div className="loading-spinner"></div> : <CheckIcon />}
              Vérifier
            </button>
            <button className="action-btn" onClick={analyzeSentiment}>
              <SentimentIcon />
              Sentiment
            </button>
            <button className="action-btn" onClick={insertSampleText}>
              <DocumentIcon />
              Exemple
            </button>
            <button
              className="action-btn"
              onClick={() => quillRef.current?.setText("")}
            >
              <DeleteIcon />
              Effacer
            </button>
          </div>
          <div id="editor-container"></div>
        </div>

        <div className="sidebar">
          <div className="feature-panel">
            <div className="panel-header">
              <div className="panel-icon">
                <ChartIcon />
              </div>
              <div className="panel-title">Statistiques</div>
            </div>
            <div className="stats-grid">
              <div className="stat-box">
                <div className="stat-number">{stats.words}</div>
                <div className="stat-label">Mots</div>
              </div>
              <div className="stat-box">
                <div className="stat-number">{stats.chars}</div>
                <div className="stat-label">Caractères</div>
              </div>
              <div className="stat-box">
                <div className="stat-number">{stats.errors}</div>
                <div className="stat-label">Erreurs</div>
              </div>
              <div className="stat-box">
                <div className="stat-number">{accuracy}%</div>
                <div className="stat-label">Précision</div>
              </div>
            </div>
          </div>

          <div className="feature-panel">
            <div className="feature-tabs">
              <button
                className={`tab-button ${activeTab === "spell" ? "active" : ""}`}
                onClick={() => setActiveTab("spell")}
              >
                <CheckIcon />
                Orthographe
              </button>
              <button
                className={`tab-button ${activeTab === "sentiment" ? "active" : ""}`}
                onClick={() => setActiveTab("sentiment")}
              >
                <SentimentIcon />
                Sentiment
              </button>
              <button
                className={`tab-button ${activeTab === "word" ? "active" : ""}`}
                onClick={() => setActiveTab("word")}
              >
                <BookIcon />
                Mot
              </button>
            </div>

            <div className="results-container">
              {activeTab === "spell" && (
                <>
                  {!spellCheckResults ? (
                    <div className="empty-state">
                      <div className="empty-state-icon">
                        <DocumentIcon />
                      </div>
                      <div className="empty-state-text">
                        Cliquez sur "Vérifier" pour analyser le texte
                      </div>
                    </div>
                  ) : (
                    spellCheckResults.results.map((result, idx) => (
                      <div
                        key={idx}
                        className={`result-item ${result.is_correct ? "correct" : "error"}`}
                      >
                        <div className="result-word">
                          {result.word}
                          <span
                            className={`badge ${result.is_correct ? "badge-success" : "badge-error"}`}
                          >
                            {result.is_correct ? "Correct" : "Erreur"}
                          </span>
                        </div>
                        {!result.is_correct && result.suggestions?.length > 0 && (
                          <div className="suggestions-list">
                            {result.suggestions.map((sug, i) => (
                              <span
                                key={i}
                                className="suggestion-tag"
                                onClick={() => replaceWord(result.word, sug.word)}
                              >
                                {sug.word}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))
                  )}
                </>
              )}

              {activeTab === "sentiment" && (
                <>
                  {!sentiment ? (
                    <div className="empty-state">
                      <div className="empty-state-icon">
                        <SentimentIcon />
                      </div>
                      <div className="empty-state-text">
                        Cliquez sur "Sentiment" pour analyser le ton
                      </div>
                    </div>
                  ) : (
                    <>
                      <div className={`sentiment-display ${sentiment.sentiment}`}>
                        <div className="sentiment-icon">
                          {getSentimentIcon(sentiment.sentiment)}
                        </div>
                        <div className="sentiment-text">{sentiment.sentiment}</div>
                        <div className="sentiment-score">Score: {sentiment.score}</div>
                      </div>
                      <div className="sentiment-details">
                        <p>
                          <strong>Mots positifs:</strong> {sentiment.positive_words}
                        </p>
                        <p>
                          <strong>Mots négatifs:</strong> {sentiment.negative_words}
                        </p>
                      </div>
                    </>
                  )}
                </>
              )}

              {activeTab === "word" && (
                <>
                  {!selectedWord ? (
                    <div className="empty-state">
                      <div className="empty-state-icon">
                        <BookIcon />
                      </div>
                      <div className="empty-state-text">
                        Sélectionnez un mot dans le texte pour l'analyser
                      </div>
                    </div>
                  ) : (
                    <div className="word-analysis">
                      <div className="analysis-word">
                        <BookIcon />
                        {selectedWord}
                      </div>

                      {lemma && (
                        <div className="analysis-section">
                          <div className="analysis-label">
                            <LinkIcon />
                            Racine (Lemme)
                          </div>
                          <div className="analysis-value">
                            {lemma.root || "Non trouvée"}
                          </div>
                          {lemma.prefixes?.length > 0 && (
                            <div
                              style={{
                                marginTop: "8px",
                                fontSize: "13px",
                                color: "#64748b",
                              }}
                            >
                              Préfixes: {lemma.prefixes.join(", ")}
                            </div>
                          )}
                        </div>
                      )}

                      {translation?.found && (
                        <div className="analysis-section">
                          <div className="analysis-label">
                            <TranslateIcon />
                            Traduction (FR)
                          </div>
                          <div className="analysis-value">
                            {translation.translation}
                          </div>
                        </div>
                      )}

                      {phonotactics && (
                        <div className="analysis-section">
                          <div className="analysis-label">
                            <SoundIcon />
                            Phonotactique
                          </div>
                          <div className="analysis-value">
                            {phonotactics.is_valid ? "✓ Valide" : "✗ Invalide"}
                          </div>
                        </div>
                      )}

                      {knowledgeGraph?.found && (
                        <div className="analysis-section">
                          <div className="analysis-label">
                            <LinkIcon />
                            Concepts liés
                          </div>
                          <div className="related-tags">
                            {knowledgeGraph.direct_relations.map((rel, i) => (
                              <span
                                key={i}
                                className="related-tag"
                                onClick={() => analyzeWord(rel)}
                              >
                                {rel}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};