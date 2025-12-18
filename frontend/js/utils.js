// Utility Functions

window.Utils = {
  updateStats: (content, spellCheckResults = null) => {
    const words = content
      .trim()
      .split(/\s+/)
      .filter((w) => w.length > 0);
    
    return {
      words: words.length,
      chars: content.length,
      errors: spellCheckResults?.errors_found || 0,
    };
  },

  calculateAccuracy: (stats) => {
    return stats.words > 0
      ? Math.round((1 - stats.errors / stats.words) * 100)
      : 0;
  },

  getSampleText: () => {
    return `Ny fianakaviana dia zavatra lehibe eto Madagasikara. Ny razana dia hajain'ny Malagasy. Manao famadihana isika mba hanomezana voninahitra ny razantsika. Tsara ny sakafo malagasy toy ny vary amin'ny laoka.`;
  }
};