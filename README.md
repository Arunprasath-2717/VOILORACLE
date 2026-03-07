# 🔮 VEILORACLE — AI-Powered Global Intelligence Network

> Real-time news intelligence across **ALL** global sectors — finance, technology, sports, entertainment, science, defense, healthcare, environment, education, agriculture, fashion, legal, and more — powered by an **Advanced 13-Engine AI Pipeline**.

---

## 🚀 Overview & Architecture (v2.0)
The VEILORACLE system is an enterprise-grade NLP pipeline that continuously streams, processes, and analyzes global news and events in real-time. It completely bypasses basic integrations in favor of fully local, highly accurate **Hugging Face Transformers** combined with multi-source global API aggregations.

### Core Architecture Components:
- **Streaming Pipeline Engine**: Designed to asynchronously pull global data and route it through 13 separate AI stages, utilizing an optional **Redis Message Queue** (gracefully falling back to memory queues if Redis is unavailable).
- **Intelligent Database Systems**: Powered by SQLite locally, scalable to **PostgreSQL with JSON/pgvector** embeddings for massive data throughput.
- **Event Lifecycle Classifier**: Determines whether an event is Emerging, Trending, Peak, or Declining based on exponential time decay calculations.
- **Deduplication Engine**: Cleans massive data influxes via Cosine Similarity (`> 0.95`).
- **Source Credibility Subsystem**: Mathematically weights outcomes based on the trusted reputation of news outlets.

---

## 📡 Live Global Data Collection (The Workflow)
VEILORACLE pulls raw, unstructured data from across the globe every few minutes, aggregating thousands of live data streams into a single unified pipeline. 

**Data Fetching Sources Include:**
1. **GNews API**: High velocity, global top headlines.
2. **WorldNews API**: Geopolitical intelligence and deep regional events.
3. **TheNews API**: Top international headlines across categories.
4. **Webz.io API**: Deep web, unstructured news crawling.
5. **NewsData.io**: Broad diverse news aggregation.
6. **GDELT Raw Files**: The Global Database of Events, Language, and Tone.
7. **NewsAPI & RSS Feeds**: Traditional media & robust fallback pipelines.

**The Workflow:**
`Data Collectors` → `Queue Manager` → `NLP Preprocessors` → `AI Event Detection & Deduplication` → `Sentiment Models` → `NER Engines` → `Sector Classifiers` → `Model Routing (LLMs)` → `Transformers (Summarization)` → `Intelligence Scoring` → `Anomaly Detection` → `Trend Forecasting` → `Database` → `React Frontend`

---

## 🛠 Complete Technology Stack

### Backend
- **Python 3.10+**: Core backend scripting and AI pipeline construction.
- **FastAPI**: Asynchronous API endpoints serving real-time AI outputs to the frontend.
- **Uvicorn**: Lightning-fast ASGI web server.
- **Redis**: Streaming message queues for high-velocity intelligence throughput.
- **SQLite / PostgreSQL (pgvector)**: Relational & Vector-based database storage.
- **SQLAlchemy & Databases (async module)**: System database interaction.
- **ThreadPoolExecutor / multi-threading**: Concurrent background scraping.
- **Requests & Feedparser**: Robust API and RSS retrievers.

### Frontend
- **React.js (Vite)**: Lightning fast, reactive frontend UI.
- **React Three Fiber & Drei**: 3D Neural visualizations and dynamic particle spheres.
- **Recharts**: Advanced data visualization, trend graphs, and sentiment distributions.
- **Vanilla CSS (Glassmorphism)**: Premium dark themes, micro-animations, and dynamic visual styling.
- **Framer Motion**: Smooth component transitions and UI animations.

---

## 🧠 Cutting-Edge AI Technologies Used (The 13 Engines)

| # | AI Engine / Module | Technology / Model Used | Purpose within Pipeline |
|---|-----------|---------|---------|
| 1 | **Vector Embeddings** | `BAAI/bge-small-en-v1.5` | Converts text into 384-dimensional dense vectors for semantic similarity mapping. |
| 2 | **Dynamic Clustering** | `hdbscan` | Highly accurate, density-based event grouping. Identifies clusters of related global news. |
| 3 | **Sentiment Analysis** | `cardiffnlp/twitter-roberta-base-sentiment` | State-of-the-art RoBERTa model for nuanced Positive/Negative/Neutral classifications. |
| 4 | **Fake News Detection** | `roberta-base-openai-detector` | Natively flags suspected disinformation and propaganda in real-time. |
| 5 | **Multilingual Engine** | `facebook/xlm-roberta-base` | Zero-shot cross-lingual analysis mapping foreign texts into contextual English embeddings. |
| 6 | **Topic Discovery** | `BERTopic` | Automatically extracts hidden, overarching themes spanning global data streams dynamically. |
| 7 | **Sector AI Routing** | `FinBERT`, `Qwen2`, `Mistral`, `Llama-3`, `BioGPT` | Intelligent semantic routing. It pipelines queries to specialized LLMs based on their sector. |
| 8 | **AI Summarization** | `google/pegasus-xsum` | Generates highly abstractive, human-quality summaries out of large event clusters. |
| 9 | **Entity Extraction** | `spaCy` (`en_core_web_sm`) | Extracts people, organizations, locations, and monetary values (NER). |
| 10| **Anomaly Detection** | Custom Z-Score Mathematics | Detects unusual volume spikes and sentiment velocity shifts. |
| 11| **Trend Forecasting** | Linear Regression | Predicts future sentiment trajectories per sector. |
| 12| **Impact Prediction** | Sector Mapping | Maps articles against 3000 distinct sectors to predict global directionality. |
| 13| **Intelligence Scoring**| Time-Decay Math Methods | Uses half-life calculations, credibility multipliers, and cluster density formulas to rank events. |

---

## 📁 Full Project Structure 

```text
VEILORACLE EE Project/
├── backend/
│   ├── api.py              # FastAPI real-time endpoints 
│   ├── pipeline.py         # 13-step Async Streaming AI pipeline orchestrator
│   ├── queue_manager.py    # Redis/Memory streaming queue layer
│   ├── database.py         # SQLite / PostgreSQL Vector storage layer
│   ├── collector.py        # Vast news collection engines (GNews, Webz.io, etc)
│   ├── config.py           # Keys, definitions, & 3000 mapped sectors
│   ├── preprocessor.py     # Initial NLP text pre-processing
│   ├── detector.py         # AI: HDBSCAN Event Clustering, Deduplication, & Lifecycle
│   ├── sentiment.py        # AI: RoBERTa Sentiment Analysis
│   ├── ner_engine.py       # AI: spaCy named entity recognition
│   ├── fake_news.py        # AI: RoBERTa Disinformation / Fake News detection
│   ├── multilingual.py     # AI: XLM-RoBERTa cross-lingual context mapping
│   ├── topic_discovery.py  # AI: BERTopic dynamic cluster discovery 
│   ├── summarizer.py       # AI: PEGASUS Abstractive Summarization
│   ├── predictor.py        # AI: Sector impact predictions & modeling
│   ├── trend_engine.py     # AI: Linear regression trend forecasting algorithms
│   ├── anomaly_engine.py   # AI: Z-score velocity anomaly detection
│   ├── sector_router.py    # Routing text queries directly into their related sectors
│   └── model_router.py     # Pipelines sector texts to matching custom Hugging Face LLMs
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Highly reactive 6-tabbed visual component application
│   │   ├── components/     # Pre-rendered interface sub-systems
│   │   ├── App.css         # Premium glassmorphism & dynamic design layers
│   │   └── index.css       # Core variable design tokens
│   └── index.html          # Standard HTML entry point
├── main.py                 # Core CLI entry point (Run pipeline, server, or UI)
├── docker-compose.yml      # Enterprise deployment stack configs (Postgres + Redis)
├── requirements.txt        # Large Python Dependency requirements
└── .env                    # System API configurations (News, Hugging Face, etc)
```

---

## 🌐 Global Sector Coverage

VEILORACLE automatically parses documents and binds them to over **3000+ AI-generated sectors** across every major field of human knowledge:
- 💰 **Finance & Economy**: Banking, Crypto, Insurance, Venture Capital
- 💻 **Technology**: Cybersecurity, AI, Cloud Computing, Semiconductors
- 🏥 **Healthcare & Bio**: Pharma, Medical Devices, Biotech, Mental Health
- ⚡ **Energy**: Renewables, Nuclear, Oil & Gas, Grid Systems
- 🏛️ **Politics & Defense**: Diplomacy, Intelligence, Law, Sanctions
- 🏈 **Sports & Entertainment**: Olympics, Football, Film, Gaming, Music
- 🔬 **Science & Space**: Physics, Astronomy, Marine Biology
- 🌍 **Environment**: Climate, Wildlife, Conservation, Clean Energy
... and thousands more granular categories dynamically tracked.

---

## 🖥️ Extravagant UI/Frontend Features

- **3D Neural Visualization** — A fully interactive React Three Fiber particle sphere showing active data clusters processing in real-time.
- **AI Intelligence Briefing** — Immediate real-time global market mood analysis outputs based on current world events.
- **6 Tabbed Dashboard Views** — Clean UX mapping across `Overview`, `Sectors`, `Events`, `NER Entities`, `AI Trends`, and `Anomalies`.
- **Global Entity Cloud** — A dynamically animated cloud mapping the people, locations, and organizations most deeply active in the news.
- **Live Trend Forecasting** — Rising and falling sector predictions accompanied by deep confidence scores.
- **Anomaly Pulse Alerts** — Automatic critical and warning indicators matching high severity metric scores against standard baselines.
- **Adaptive Glassmorphism** — Premium dark themes layered with micro-animations and blurred glass visual depths.

---

## 🚀 Quick Start Guide

**1. Install Python Backend Dependencies:**
```bash
pip install -r requirements.txt
```

**2. Download NLP Reference Core (for Named Entity Extraction):**
```bash
python -m spacy download en_core_web_sm
```

**3. Configure your API resources:**
Check `.env` and fill in necessary elements (e.g. `GEMINI_API_KEY`, `GNEWS_API_KEY`, `HF_API_TOKEN`, etc.)

**4. Start background Database/Queue Systems (Optional but recommended):**
```bash
docker-compose up -d
```
*(If skipped, VEILORACLE simply falls back to standard SQLite databases and memory-based array queues).*

**5. Install UI Frontend Dependencies:**
```bash
cd frontend
npm install
cd ..
```

**6. Spin up the entire VEILORACLE System:**

Option A: Run the streaming intelligence AI pipeline continuously in the background (CLI 1)
```bash
python main.py pipeline --loop
```

Option B: Start the backend FastAPI data server (CLI 2)
```bash
python main.py server
```

Option C: Bring the React interface to life (CLI 3)
```bash
python main.py frontend
```

*Open your local browser to `http://localhost:5173/` to view the running orchestration!*
