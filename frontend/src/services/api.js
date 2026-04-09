/**
 * Kronaxis API Service
 * Centralized data fetching from FastAPI backend
 */

const API_BASE = import.meta.env.VITE_API_URL || '/api';
const WS_BASE = import.meta.env.VITE_WS_URL || (window.location.protocol === 'https:' ? 'wss:' : 'ws:') + '//' + window.location.host + '/ws';

function getMockDataFor(endpoint) {
  if (endpoint.includes('/metrics')) {
    return {
      sentiment_distribution: { Positive: 45, Neutral: 35, Negative: 20 },
    };
  }
  if (endpoint.includes('/events')) {
    return Array.from({ length: 10 }).map((_, i) => ({
      label: `Global Tech Summit ${i + 1}`,
      size: Math.floor(Math.random() * 50) + 10,
      importance_score: Math.random(),
    }));
  }
  if (endpoint.includes('/articles')) {
    return Array.from({ length: 15 }).map((_, i) => ({
      title: `Global Economic Intelligence Update ${i + 1} - Market Impacts`,
      source: ['NewsData.io', 'GDELT', 'World News API', 'RSS Matrix'][i % 4],
      published_at: new Date(Date.now() - Math.floor(Math.random() * 8600000)).toISOString(),
      sentiment_label: ['Positive', 'Neutral', 'Negative'][i % 3],
      sentiment_score: (Math.random() * 2) - 1,
      language: 'en'
    }));
  }
  if (endpoint.includes('/impacts')) {
    return Array.from({ length: 20 }).map((_, i) => ({
      sector: ['Technology', 'Finance', 'Healthcare', 'Energy', 'Retail', 'Education', 'Automotive', 'RealEstate'][i % 8] + (i > 7 ? ' Sub' : ''),
      bullish: Math.floor(Math.random() * 20),
      bearish: Math.floor(Math.random() * 20),
    }));
  }
  if (endpoint.includes('/entities')) {
    return {
      ORG: [{text: "Tesla", count: 85}, {text: "OpenAI", count: 112}, {text: "Nvidia", count: 94}],
      GPE: [{text: "United States", count: 65}, {text: "European Union", count: 45}, {text: "China", count: 78}],
      EVENT: [{text: "Tech Summit 2026", count: 32}, {text: "Global Trade Pact", count: 28}],
      PRODUCT: [{text: "Quantum Processors", count: 41}, {text: "Auto-GPT 5", count: 56}]
    };
  }
  if (endpoint.includes('/trends')) {
    return [
      { sector: "AI Infrastructure", direction: "up", score: 0.94, trend: "Bullish" },
      { sector: "Commercial Real Estate", direction: "down", score: 0.88, trend: "Bearish" },
      { sector: "Cybersecurity Software", direction: "up", score: 0.91, trend: "Bullish" },
      { sector: "Renewable Energy", direction: "up", score: 0.85, trend: "Bullish" },
      { sector: "Consumer Retail", direction: "down", score: 0.72, trend: "Bearish" },
    ];
  }
  if (endpoint.includes('/sectors')) {
    return { sectors: [
      { sector: "Technology", count: 120, percentage: 35 },
      { sector: "Finance", count: 80, percentage: 25 },
      { sector: "Healthcare", count: 60, percentage: 20 },
      { sector: "Energy", count: 40, percentage: 15 }
    ]};
  }
  if (endpoint.includes('/anomalies')) {
    return [
      { id: '1', title: 'Volume Surge: Quantum Tech', severity: 'High', description: '400% abnormal latency spike in patent node submissions mapped to quantum computing.', timestamp: new Date().toISOString(), type: 'volume' },
      { id: '2', title: 'Market Sentiment Crash', severity: 'Critical', description: 'Negative NLP sentiment threshold exceeded across 15+ trusted financial news outlets.', timestamp: new Date(Date.now() - 3600000).toISOString(), type: 'sentiment' },
      { id: '3', title: 'Emerging Supply Chain Risk', severity: 'Medium', description: 'Semiconductor routing disruption flagged via real-time logistics clustering.', timestamp: new Date(Date.now() - 8600000).toISOString(), type: 'pattern' },
      { id: '4', title: 'Geopolitical Shift Detected', severity: 'High', description: 'Unusual correlation density found between new energy tariffs and bilateral statements.', timestamp: new Date(Date.now() - 14400000).toISOString(), type: 'correlation' },
    ];
  }
  if (endpoint.includes('/geo-news')) {
    const keywords = [
      "Technology", "Cybersecurity", "Artificial Intelligence", "Blockchain",
      "Politics", "Elections", "Diplomacy", "Legislation",
      "Economy", "Markets", "Trade", "Inflation",
      "Environment", "Climate Change", "Renewable Energy", "Natural Disasters",
      "Healthcare", "Pandemics", "Pharmaceuticals", "Medical Research",
      "Security", "Crime", "Military", "Terrorism", "Logistics", "Energy"
    ];
    const generateId = () => Math.random().toString(36).substr(2, 9);
    const makeNews = (count, location) => Array.from({ length: count }).map(() => {
      const k1 = keywords[Math.floor(Math.random() * keywords.length)];
      const k2 = keywords[Math.floor(Math.random() * keywords.length)];
      return {
        id: generateId(),
        title: `${k1} developments escalate in ${location}`,
        summary: `Recent reports indicate significant movement regarding ${k1.toLowerCase()} and ${k2.toLowerCase()} in the region. Monitoring is advised.`,
        keywords: [k1, k2],
        sentiment: Math.random() > 0.5 ? 'Positive' : 'Negative',
        time: new Date(Date.now() - Math.random() * 86400000).toISOString(),
        score: (Math.random() * 100).toFixed(1)
      };
    });

    return {
      keywords,
      regions: [
        {
          id: 'usa', name: 'United States', code: 'US',
          news: makeNews(5, 'United States'),
          states: [
            {
              id: 'ca', name: 'California', news: makeNews(4, 'California'),
              districts: [
                { id: 'sf', name: 'San Francisco', news: makeNews(3, 'San Francisco') },
                { id: 'sc', name: 'Santa Clara', news: makeNews(2, 'Santa Clara') }
              ]
            },
            {
              id: 'ny', name: 'New York', news: makeNews(3, 'New York'),
              districts: [
                { id: 'mh', name: 'Manhattan', news: makeNews(4, 'Manhattan') },
                { id: 'br', name: 'Brooklyn', news: makeNews(2, 'Brooklyn') }
              ]
            }
          ]
        },
        {
          id: 'ind', name: 'India', code: 'IN',
          news: makeNews(4, 'India'),
          states: [
            {
              id: 'tn', name: 'Tamil Nadu', news: makeNews(5, 'Tamil Nadu'),
              districts: [
                { id: 'ch', name: 'Chennai', news: makeNews(6, 'Chennai') },
                { id: 'cb', name: 'Coimbatore', news: makeNews(2, 'Coimbatore') }
              ]
            },
            {
              id: 'mh', name: 'Maharashtra', news: makeNews(3, 'Maharashtra'),
              districts: [
                { id: 'mu', name: 'Mumbai', news: makeNews(5, 'Mumbai') },
                { id: 'pu', name: 'Pune', news: makeNews(2, 'Pune') }
              ]
            }
          ]
        },
        {
          id: 'uk', name: 'United Kingdom', code: 'GB',
          news: makeNews(3, 'United Kingdom'),
          states: [
            {
              id: 'eng', name: 'England', news: makeNews(4, 'England'),
              districts: [
                { id: 'ldn', name: 'Greater London', news: makeNews(7, 'London') },
                { id: 'man', name: 'Manchester', news: makeNews(3, 'Manchester') }
              ]
            }
          ]
        }
      ]
    };
  }
  return [];
}

async function fetchJSON(endpoint) {
  try {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 115000); // 115 seconds to allow ultra-heavy OSINT API fetches
    const res = await fetch(`${API_BASE}${endpoint}`, { signal: controller.signal });
    clearTimeout(id);
    if (!res.ok) throw new Error(`API ${endpoint} failed: ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn(`Fallback triggered for ${endpoint} due to:`, error.message);
    return getMockDataFor(endpoint);
  }
}

/* ── Core Endpoints ─────────────────────────────────────── */

export async function getMetrics() {
  return fetchJSON('/metrics');
}

export async function getEvents(limit = 25) {
  return fetchJSON(`/events?limit=${limit}`);
}

export async function getArticles(limit = 100) {
  return fetchJSON(`/articles?limit=${limit}`);
}

export async function getArticlesBySector(sector, limit = 50) {
  return fetchJSON(`/articles/sector/${encodeURIComponent(sector)}?limit=${limit}`);
}

export async function getImpacts() {
  return fetchJSON('/impacts');
}

export async function getStatus() {
  return fetchJSON('/status');
}

export async function getPipelineRuns(limit = 5) {
  return fetchJSON(`/pipeline_runs?limit=${limit}`);
}

export async function getGeoNews(query = null) {
  if (query) {
    return fetchJSON(`/geo-news?query=${encodeURIComponent(query)}`);
  }
  return fetchJSON('/geo-news');
}

/* ── AI Endpoints ───────────────────────────────────────── */

export async function getEntities() {
  return fetchJSON('/ai/entities');
}

export async function getTrends() {
  return fetchJSON('/ai/trends');
}

export async function getAnomalies() {
  return fetchJSON('/ai/anomalies');
}

export async function getAISummary() {
  return fetchJSON('/ai/summary');
}

export async function getSectorDistribution() {
  return fetchJSON('/ai/sectors');
}

export async function getAIModels() {
  return fetchJSON('/ai/models');
}

export async function getIntelligence(limit = 25) {
  return fetchJSON(`/ai/intelligence?limit=${limit}`);
}

export async function analyzeText(text, title = '') {
  const res = await fetch(`${API_BASE}/ai/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, title }),
  });
  if (!res.ok) throw new Error(`Analyze failed: ${res.status}`);
  return res.json();
}

export async function sendChatMessage(message) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error(`Chat failed: ${res.status}`);
  return res.json();
}

export async function getAlerts(hours = 6) {
  return fetchJSON(`/alerts?hours=${hours}`);
}

/* ── WebSocket ──────────────────────────────────────────── */

export function connectWebSocket(onMessage, onError) {
  const ws = new WebSocket(WS_BASE);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (e) {
      console.error('WS parse error:', e);
    }
  };

  ws.onerror = (event) => {
    console.error('WS error:', event);
    if (onError) onError(event);
  };

  ws.onclose = () => {
    // Auto-reconnect after 5s
    setTimeout(() => connectWebSocket(onMessage, onError), 5000);
  };

  return ws;
}
