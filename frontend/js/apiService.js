// API Service Module
const API_BASE = "http://localhost:8000";

window.ApiService = {
  spellCheck: async (text) => {
    const response = await fetch(`${API_BASE}/spell-check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    return await response.json();
  },

  analyzeSentiment: async (text) => {
    const response = await fetch(`${API_BASE}/sentiment`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    return await response.json();
  },

  lemmatizeWord: async (word) => {
    const response = await fetch(`${API_BASE}/lemmatize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ word }),
    });
    return await response.json();
  },

  getKnowledgeGraph: async (word) => {
    const response = await fetch(`${API_BASE}/knowledge-graph`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ word }),
    });
    return await response.json();
  },

  translateWord: async (word, sourceLang = "mg", targetLang = "fr") => {
    const response = await fetch(`${API_BASE}/translate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        word,
        source_lang: sourceLang,
        target_lang: targetLang,
      }),
    });
    return await response.json();
  },

  validatePhonotactics: async (word) => {
    const response = await fetch(`${API_BASE}/validate-phonotactics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ word }),
    });
    return await response.json();
  }
};