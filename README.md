<p align="center">
  <img src="frontend/src/Logo.png" alt="Kronaxis Logo" width="120" />
</p>

<h1 align="center">🔮 Kronaxis — AI-Powered Real-Time Global Intelligence Network</h1>

<p align="center">
  <strong>Enterprise-Grade NLP Pipeline</strong> · <strong>13 AI Engines</strong> · <strong>8 Data Sources</strong> · <strong>3000+ Sectors</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/react-18.2-61DAFB?style=flat-square&logo=react&logoColor=white" />
  <img src="https://img.shields.io/badge/fastapi-0.109-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/pytorch-2.1-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/huggingface-transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/vite-5.1-646CFF?style=flat-square&logo=vite&logoColor=white" />
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Data Sources & API Integrations](#-data-sources--api-integrations)
- [The 13 AI Engines](#-the-13-ai-engines)
- [Tech Stack](#-complete-technology-stack)
- [Project Structure](#-project-structure)
- [Sector Coverage](#-global-sector-coverage)
- [Frontend Dashboard](#-intelligent-dashboard)
- [Quick Start](#-quick-start-guide)
- [Environment Variables](#-environment-variables)
- [CLI Commands](#-cli-commands)

---

## 🚀 Overview

Kronaxis is an **enterprise-grade, real-time global news intelligence system** that continuously streams, processes, and analyzes world events across every domain — finance, technology, sports, entertainment, science, defense, healthcare, environment, education, agriculture, fashion, legal, and more.

It combines **8 live data source APIs** with a **13-stage AI pipeline** built on state-of-the-art Hugging Face Transformers, spaCy NER, HDBSCAN clustering, BERTopic discovery, and custom anomaly detection — all served through a **premium React dashboard** with real-time visualizations, semantic search, and glassmorphism aesthetics.

### Key Capabilities

| Capability | Description |
|---|---|
| 🌐 **Multi-Source Aggregation** | Pulls from 8 global APIs + 18 RSS feeds simultaneously |
| 🧠 **13-Engine AI Pipeline** | Sentiment, NER, fake news detection, topic discovery, anomaly detection, trend forecasting |
| 📊 **Real-Time Analytics** | Interactive donut charts, trajectory maps, entity classification, sector analysis |
| 🔍 **Semantic Search** | Full-text and vector-based search powered by Supabase |
| 🎯 **3000+ Sector Classification** | AI-generated sector taxonomy covering every global industry |
| 🛡️ **Fake News Detection** | RoBERTa-based disinformation classifier |
| 📈 **Trend Forecasting** | Linear regression models predicting sector momentum |
| ⚡ **Streaming Architecture** | Redis-backed message queues with in-memory fallback |

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        VEILORACLE INTELLIGENCE PIPELINE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    📡 DATA COLLECTION LAYER                      │       │
│  │  GNews · NewsData · WorldNews · TheNews · Webz.io               │       │
│  │  NewsAPI · GDELT · 18 RSS Feeds (BBC, NPR, Al Jazeera, etc.)   │       │
│  └───────────────────────────┬──────────────────────────────────────┘       │
│                              ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    📨 MESSAGE QUEUE (Redis / Memory)              │       │
│  └───────────────────────────┬──────────────────────────────────────┘       │
│                              ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    🧠 13-STAGE AI PROCESSING                     │       │
│  │                                                                   │       │
│  │  1. NLP Preprocessing ──▶ 2. Fake News Detection                 │       │
│  │  3. Multilingual NLP ───▶ 4. Event Clustering (HDBSCAN)         │       │
│  │  5. Sentiment (RoBERTa) ▶ 6. Named Entity Recognition          │       │
│  │  7. Sector Classification ▶ 8. LLM Model Routing               │       │
│  │  9. Abstractive Summary ─▶ 10. Impact Prediction                │       │
│  │  11. Intelligence Score ─▶ 12. Anomaly Detection                │       │
│  │  13. Trend Forecasting                                           │       │
│  └───────────────────────────┬──────────────────────────────────────┘       │
│                              ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    💾 STORAGE LAYER                               │       │
│  │  SQLite (local) · PostgreSQL (production) · Supabase (cloud)    │       │
│  └───────────────────────────┬──────────────────────────────────────┘       │
│                              ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    🖥️ PRESENTATION LAYER                         │       │
│  │  FastAPI REST + WebSocket ──▶ React 18 + Recharts + Framer      │       │
│  └──────────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Core Architecture Components

| Component | Purpose |
|---|---|
| **Streaming Pipeline Engine** | Asynchronously pulls global data through 13 AI stages. Uses Redis message queue with graceful in-memory fallback. |
| **Intelligent Database Systems** | SQLite locally, scalable to PostgreSQL with JSON/pgvector and Supabase cloud sync. |
| **Event Lifecycle Classifier** | Categorizes events as Emerging, Trending, Peak, or Declining via exponential time decay. |
| **Deduplication Engine** | Cosine similarity threshold (>0.95) removes duplicate articles across sources. |
| **Source Credibility Subsystem** | Weights outcomes based on outlet trust scores (Reuters 0.95, BBC 0.90, Bloomberg 0.92, etc.). |

---

## 📡 Data Sources & API Integrations

Kronaxis aggregates from **8 distinct API sources** plus an extensive RSS feed network:

| # | Source | Type | What It Provides |
|---|--------|------|------------------|
| 1 | **GNews API** | Paid | Top headlines across general, world, business, technology categories (10 articles/category) |
| 2 | **NewsData.io** | Paid | Latest global news with language filtering, up to 50 articles per call |
| 3 | **WorldNews API** | Paid | Full-text search with `breaking OR latest` queries, up to 50 results |
| 4 | **Webz.io** | Paid | News API Lite — broad web crawling for news content |
| 5 | **NewsAPI** | Freemium | Multi-category headlines (general, tech, business, science, health, sports, entertainment) |
| 6 | **GDELT** | Free | Global Event Database — real-time global event monitoring (capped at 25 to prevent feed dominance) |
| 7 | **RSS Feeds** | Free | 18+ enterprise feeds: Reuters, BBC, NPR, Guardian, TechCrunch, Verge, WSJ + regional coverage |

### Collection Pipeline
```
All 8 Sources → Deduplication (title similarity) → Source Breakdown Report → Queue Manager
```

After every collection cycle, a detailed **source breakdown report** is logged showing exactly how many articles each source contributed.

---

## 🧠 The 13 AI Engines

| # | Engine | Model / Technology | Purpose |
|---|--------|--------------------|---------|
| 1 | **Vector Embeddings** | `BAAI/bge-small-en-v1.5` | Converts text to 384-dimensional dense vectors for semantic similarity |
| 2 | **Dynamic Clustering** | `HDBSCAN` | Density-based event grouping — no predetermined cluster count needed |
| 3 | **Sentiment Analysis** | `cardiffnlp/twitter-roberta-base-sentiment` | Fine-tuned RoBERTa model for Positive / Negative / Neutral classification |
| 4 | **Fake News Detection** | `roberta-base-openai-detector` | Disinformation and AI-generated text detection |
| 5 | **Multilingual NLP** | `facebook/xlm-roberta-base` | Zero-shot cross-lingual language detection and mapping |
| 6 | **Topic Discovery** | `BERTopic` | Automatic hidden theme extraction using transformer embeddings + UMAP |
| 7 | **Sector AI Routing** | Custom Keyword Mapping | Routes articles to 3000+ sectors using weighted keyword matching |
| 8 | **AI Summarization** | `google/pegasus-xsum` | Abstractive, human-quality event summaries |
| 9 | **Entity Extraction** | `spaCy` (`en_core_web_sm`) | Named Entity Recognition — PERSON, ORG, GPE, LOC, DATE, MONEY |
| 10 | **Anomaly Detection** | Custom Z-Score Engine | Flags volume spikes and sentiment shift anomalies (Critical / Warning / Normal) |
| 11 | **Trend Forecasting** | Linear Regression | Predicts future sentiment trajectories and sector momentum |
| 12 | **Impact Prediction** | Sector Mapping Vectors | Matches articles against 3000 sectors with confidence scoring |
| 13 | **Intelligence Scoring** | Time-Decay (Half-Life) | Calculates event importance using exponential decay and source credibility weighting |

### Sector-Specific LLM Routing

For deeper analysis, articles are routed to **domain-specialized large language models**:

| Sector | Model |
|--------|-------|
| Finance | `ProsusAI/finbert` |
| Technology | `Qwen/Qwen2-7B-Instruct` |
| Politics | `mistralai/Mistral-7B-Instruct-v0.3` |
| Business | `deepseek-ai/deepseek-llm-7b-chat` |
| Healthcare | `microsoft/BioGPT-Large` |
| General | `meta-llama/Llama-3-8B-Instruct` |

---

## 🛠 Complete Technology Stack

### Backend (Python)

| Technology | Version | Role |
|------------|---------|------|
| **Python** | 3.10+ | Core backend language |
| **FastAPI** | ≥0.109 | Asynchronous REST API + WebSocket endpoints |
| **Uvicorn** | ≥0.27 | ASGI web server |
| **PyTorch** | ≥2.1 | Deep learning framework for transformer models |
| **Hugging Face Transformers** | ≥4.36 | Pre-trained NLP model loading and inference |
| **Sentence-Transformers** | ≥2.3 | Embedding generation (BGE-small-en) |
| **spaCy** | ≥3.7 | Named Entity Recognition |
| **HDBSCAN** | ≥0.8 | Density-based clustering |
| **BERTopic** | ≥0.15 | Neural topic modeling |
| **scikit-learn** | ≥1.4 | ML utilities, cosine similarity, regression |
| **NLTK** | ≥3.8 | Text tokenization and preprocessing |
| **Pandas** | ≥2.2 | Data manipulation and analysis |
| **NumPy** | ≥1.26 | Numerical computing |
| **Requests** | ≥2.31 | HTTP API client |
| **Feedparser** | ≥6.0 | RSS/Atom feed parsing |
| **newsapi-python** | ≥0.2.7 | NewsAPI SDK |
| **python-dotenv** | ≥1.0 | Environment variable management |
| **Redis** | Optional | Streaming message queue (in-memory fallback) |
| **SQLite** | Built-in | Local database storage |
| **Websockets** | ≥11.0 | Real-time status updates |
| **Matplotlib / Seaborn / Plotly** | Various | Data visualization (server-side) |
| **pytest** | ≥7.4 | Testing framework |

### Frontend (React)

| Technology | Version | Role |
|------------|---------|------|
| **React** | 18.2 | Core UI library |
| **Vite** | 5.1 | Lightning-fast build tool & dev server |
| **React Router DOM** | 7.13 | Client-side routing (Landing → Dashboard) |
| **Recharts** | 3.7 | Data visualization — Pie, Bar, Area charts with custom gradients |
| **Framer Motion** | 12.36 | Smooth animations and page transitions |
| **Lucide React** | 0.344 | Premium SVG icon library |
| **React Hot Toast** | 2.6 | Notification system |
| **@supabase/supabase-js** | 2.99 | Cloud database queries and semantic search |
| **Three.js** | 0.183 | 3D rendering engine |
| **React Three Fiber** | 8.17 | React renderer for Three.js |
| **React Three Drei** | 9.122 | Three.js helpers and abstractions |
| **Globe.gl / React Globe** | 2.45 / 2.27 | 3D globe visualizations |
| **Spline Runtime** | 1.12 | 3D scene integration |
| **Vanilla CSS** | — | Glassmorphism, micro-animations, light SaaS theme |

### Infrastructure & DevOps

| Technology | Role |
|------------|------|
| **Docker Compose** | Container orchestration (Redis + PostgreSQL) |
| **Supabase** | Cloud PostgreSQL database with real-time subscriptions |
| **Redis** | Message queue for pipeline streaming |
| **Git** | Version control |
| **VS Code** | Development environment |

---

## 📁 Project Structure

```
VEILORACLE EE Project/
├── main.py                    # CLI entry point (pipeline | server | frontend)
├── requirements.txt           # Python dependencies (24 packages)
├── docker-compose.yml         # Redis + PostgreSQL containers
├── .env                       # API keys & credentials
│
├── backend/                   # Python backend (22 modules)
│   ├── __init__.py            # Package initializer
│   ├── api.py                 # FastAPI REST + WebSocket endpoints
│   ├── pipeline.py            # 13-step streaming AI pipeline orchestrator
│   ├── queue_manager.py       # Redis / in-memory message queue
│   ├── database.py            # SQLite / PostgreSQL / Supabase storage
│   ├── collector.py           # Multi-source news aggregation (8 APIs)
│   ├── config.py              # API keys, sector maps, 3000 sector generator
│   ├── preprocessor.py        # NLP text cleaning & normalization
│   ├── detector.py            # HDBSCAN event clustering + deduplication
│   ├── sentiment.py           # RoBERTa sentiment analysis
│   ├── ner_engine.py          # spaCy named entity recognition
│   ├── fake_news.py           # RoBERTa fake news / AI-text detection
│   ├── multilingual.py        # XLM-RoBERTa language detection
│   ├── topic_discovery.py     # BERTopic dynamic theme extraction
│   ├── summarizer.py          # Pegasus abstractive summarization
│   ├── anomaly_engine.py      # Z-score anomaly detection
│   ├── trend_engine.py        # Linear regression trend forecasting
│   ├── predictor.py           # Sector impact prediction
│   ├── intelligence.py        # Importance & risk scoring (time-decay)
│   ├── sector_router.py       # Keyword-based sector classification
│   ├── model_router.py        # LLM routing (FinBERT/Qwen/Mistral/etc.)
│   ├── supabase_client.py     # Supabase connection manager
│   └── supabase_manager.py    # Cloud sync orchestrator
│
├── frontend/                  # React 18 + Vite frontend
│   ├── package.json           # Node dependencies (16 packages)
│   ├── vite.config.js         # Vite build configuration
│   ├── index.html             # HTML entry point
│   └── src/
│       ├── main.jsx           # React DOM root
│       ├── App.jsx            # 6-tab intelligence dashboard (~1050 lines)
│       ├── App.css            # Dashboard styling (glassmorphism + animations)
│       ├── LandingPage.jsx    # Immersive marketing landing page
│       ├── LandingPage.css    # Landing page premium styling
│       ├── supabaseClient.js  # Frontend Supabase connection
│       ├── Logo.jpeg          # Brand logo
│       └── index.css          # CSS variable design tokens
│
├── data/                      # SQLite database storage
├── tests/                     # Test suite
└── tmp/                       # Temporary / diagnostic scripts
```

---

## 🌐 Global Sector Coverage

VEILORACLE automatically classifies every article into one or more of **3000+ dynamically generated sectors** spanning:

| Domain | Example Sectors |
|--------|----------------|
| 💰 **Finance & Economy** | Banking, Cryptocurrency, Insurance, Venture Capital |
| 💻 **Technology** | Cybersecurity, Artificial Intelligence, Cloud Computing, Semiconductors |
| 🏥 **Healthcare & Biotech** | Pharmaceuticals, Medical Devices, Biotech, Mental Health |
| ⚡ **Energy & Environment** | Renewable Energy, Nuclear, Oil & Gas, Climate |
| 🏛️ **Politics & Governance** | Diplomacy, Defense, Intelligence, Law & Justice |
| ✈️ **Transport & Logistics** | Aviation, Shipping, Automotive, Railways |
| 🛒 **Retail & Consumer** | E-Commerce, Consumer Goods, Luxury, Food & Beverage |
| 🔬 **Science & Space** | Physics, Astronomy, Marine Biology, Space |
| 📚 **Education** | Higher Education, EdTech, Research, Scholarships |
| 🎬 **Entertainment & Media** | Film, Music, Gaming, Streaming |
| 🏈 **Sports** | Football, Cricket, Basketball, Olympics |
| 🌾 **Agriculture & Food** | Farming, Fisheries, Food Processing, Organic |
| 🏗️ **Real Estate** | Construction, Architecture, Urban Planning, Housing |
| 🏭 **Manufacturing** | Robotics, Automation, Textiles, Steel |
| 📡 **Telecom & Media** | Broadcasting, Publishing, Social Media, Advertising |
| 🎨 **Arts & Culture** | Fashion, Design, Literature, Heritage |
| 🚀 **Aerospace & Defense** | Satellites, Drones, Military, Naval |
| ⛏️ **Mining & Resources** | Rare Earth, Gold, Diamond, Lithium |
| ⚖️ **Legal & Compliance** | Human Rights, Immigration, Trade Law |

Sectors are generated using a combinatorial algorithm with **base sectors × modifiers × sub-categories**, each mapped to domain-specific keyword pools.

---

## 🖥️ Intelligent Dashboard

The VEILORACLE dashboard is a **6-tab React application** built with premium SaaS aesthetics:

### Dashboard Tabs

| Tab | Content |
|-----|---------|
| **Overview** | Stat boxes (Total Articles, Events, Sources, Sectors), Global Anomaly Radar (Critical Velocity Spikes), live event feed |
| **Analytics** | Sentiment donut chart, verification donut, source volume bars, entity classification, real-time trajectory map, sector strengths/vulnerabilities |
| **Sectors** | Sector intelligence grid with momentum indicators, impact direction arrows |
| **Intel** | Named entities table (PERSON, ORG, GPE), anomaly alerts (Critical/Warning) |
| **Search** | Supabase-powered full-text search across archived articles |
| **System** | Live WebSocket system status, pipeline health, model loading states |

### Design Features
- **Premium SaaS Typography** — Replaced stock fonts with Google's `Syne` and `Outfit`, featuring iridescent text clipping masks.
- **Glassmorphism** — Frosted glass panels with `backdrop-filter: blur`, subtle glows, and seamless integration.
- **Micro-Animations** — Floating icons, hover scale/rotate effects, bounce transitions.
- **Dribbble HUD Loader** — Afro-M inspired pixel-to-pixel cybernetic loader with segmented scanning rings, a glowing neural targeted core, and `JetBrains Mono` system typography.
- **Responsive Grid** — Side-by-side chart layouts that adapt to any screen size.
- **Live Data** — Auto-refresh cycle for real-time updates direct from the backend pipeline.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) Redis for streaming queue
- (Optional) Docker for Redis + PostgreSQL

### 1. Clone & Install Backend
```bash
git clone <repository-url>
cd "VOILORACLE EE Project"
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
# News API Keys (all required for full coverage)
NEWSAPI_KEY=your_newsapi_key
NEWSDATA_API_KEY=your_newsdata_key
GNEWS_API_KEY=your_gnews_key
WORLDNEWS_API_KEY=your_worldnews_key
WEBZ_API_KEY=your_webz_key

# AI Model API
GEMINI_API_KEY=your_gemini_key

# Supabase (optional — for cloud search)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

### 3. Install Frontend
```bash
cd frontend
npm install
cd ..
```

### 4. Run the System
Open **three separate terminals**:

```bash
# Terminal 1: AI Pipeline (continuous)
python main.py pipeline --loop

# Terminal 2: Backend API Server (port 8000)
python main.py server

# Terminal 3: Frontend Dev Server (port 5173)
cd frontend && npm run dev
```

### 5. Open Dashboard
Navigate to **http://localhost:5173/** in your browser.

---

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEWSAPI_KEY` | Yes | NewsAPI.org API key |
| `NEWSDATA_API_KEY` | Yes | NewsData.io API key |
| `GNEWS_API_KEY` | Yes | GNews.io API key |
| `WORLDNEWS_API_KEY` | Yes | WorldNewsAPI.com API key |
| `WEBZ_API_KEY` | Yes | Webz.io API token |
| `GEMINI_API_KEY` | Optional | Google Gemini for advanced analysis |
| `HF_API_TOKEN` | Optional | Hugging Face API for large model inference |
| `SUPABASE_URL` | Optional | Supabase project URL |
| `SUPABASE_ANON_KEY` | Optional | Supabase anonymous key |
| `DATABASE_URL` | Optional | PostgreSQL connection string |
| `REDIS_URL` | Optional | Redis connection string (default: `redis://localhost:6379/0`) |

---

## ⌨️ CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py pipeline` | Run the 13-stage AI pipeline once (one-shot) |
| `python main.py pipeline --loop` | Run the pipeline continuously (every 180 seconds) |
| `python main.py server` | Start FastAPI backend on `http://localhost:8000` |
| `python main.py frontend` | Start React frontend on `http://localhost:5173` |

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | System health & pipeline status |
| `/api/metrics` | GET | Dashboard metrics (article count, sentiment, sources) |
| `/api/events` | GET | Detected events with summaries |
| `/api/articles` | GET | Processed articles with sentiment & entities |
| `/api/impacts` | GET | Sector impact predictions |
| `/api/ai/entities` | GET | Named entity extraction results |
| `/api/ai/trends` | GET | Sector trend analysis (rising/falling) |
| `/api/ai/anomalies` | GET | Anomaly detection alerts |
| `/ws/status` | WebSocket | Real-time system status updates |

---

<p align="center">
  Built with ❤️ using Python, React, PyTorch, and Hugging Face Transformers
</p>
