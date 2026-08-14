/**
* WebMCP Browser Registration - ZeroHype B2B Bullshit Detector
* score_bullshit proxies the live API at api.zerohypelab.com/api/score.
*/
(function () {
  'use strict';
  const MANIFEST_ULL = '/.well-known/mcp.json';
  const API_URL = 'https://api.zerohypelab.com/api/score';
  const WebMCP = {
    version: '1.0.0',
    manifestUrl: MANIFEST_URL,
    tools: {
      score_bullshit: async function (params) {
        const text = (params && params.text) || '';
        if (!text) return { status: 'error', error: 'text required' };
        const res = await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          return { status: 'error', error: err.error || ('HTTP ' + res.status) };
        }
        const data = await res.json();
        return {
          status: 'success',
          score: data.score,
          label: data.label,
          callouts: data.callouts || [],
          verdict: data.callouts && data.callouts.length
            ? 'Detected ' + data.callouts.length + ' offenders.'
            : 'Clean.'
        };
      }
    }
  };
  window.WebMCP = WebMCP;
  if (typeof window.navigator !== 'undefined') {
    window.navigator.modelContext = window.navigator.modelContext || {};
    window.navigator.modelContext.mcpManifestUrl = MANIFEST_URL;
  }
  console.log('[WebMCP] Registered ZeroHype bullshit detector.'];
})();
