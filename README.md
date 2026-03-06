# 🔮 VEILORACLE — AI-Powered Global Intelligence Network

> Real-time news intelligence across **ALL** global sectors — finance, technology, sports, entertainment, science, defense, healthcare, environment, education, agriculture, fashion, legal, and more — powered by an **Advanced 12-Engine AI Pipeline**.

---

## 🚀 Recent System Upgrades (v2.0 Architecture)
The VEILORACLE system has been completely overhauled from a basic prototype to an enterprise-grade NLP pipeline:
- **Purged Google Gemini** and VADER in favor of fully local, highly accurate **Hugging Face Transformers**.
- **Upgraded Database** to support **Vector Embeddings (JSON/pgvector)** and massive data throughput.
- **Streaming Pipeline Architecture** built with an optional **Redis Message Queue** (gracefully falling back to memory queues if Redis is unavailable).
- Built an **Event Lifecycle Classifier** (Emerging, Trending, Peak, Declining) based on exponential time decay.
- Added **Duplicate Detection** via Cosine Similarity (`> 0.95`).
- Added robust **Source Credibility Scoring** to mathematically weight trusted outlets higher.

---

## 🧠 Cutting-Edge AI Technologies Used

| # | AI Engine / Module | Technology | Purpose |
|---|-----------|---------|---------|
| 1 | **Vector Embeddings** | `BAAI/bge-small-en-v1.5` | Converts text into 384-dimensional dense vectors for semantic similarity. Upgraded from all-MiniLM. |
| 2 | **Dynamic Clustering** | `hdbscan` | Highly accurate, density-based event grouping (Upgraded from rigid DBSCAN). |
| 3 | **Sentiment Analysis** | `cardiffnlp/twitter-roberta-base-sentiment` | State-of-the-art RoBERTa model for nuanced Positive/Negative/Neutral classification. |
| 4 | **Fake News Detection** | `roberta-base-openai-detector` | Natively flags disinformation and propaganda in real-time. |
| 5 | **Multilingual Engine** | `facebook/xlm-roberta-base` | Zero-shot cross-lingual analysis mapping foreign texts into contextual embeddings. |
| 6 | **Topic Discovery** | `BERTopic` | Automatically extracts hidden, overarching themes spanning global data streams dynamically. |
| 7 | **AI Summarization** | `google/pegasus-xsum` | Generates highly abstractive, human-quality summaries of large event clusters. |
| 8 | **Entity Extraction** | `spaCy` (en_core_web_sm) | Extracts people, organizations, locations, money. |
| 9 | **Anomaly Detection** | Custom Z-Score Math | Detects unusual volume spikes and sentiment velocity shifts. |
| 10| **Trend Forecasting** | Linear Regression | Predicts future sentiment direction per sector. |
| 11| **Impact Prediction** | Sector Mapping | Maps articles → 3000 sectors, predicts global directionality. |
| 12| **Intelligence Scoring**| Time-Decay Math | Uses half-life calculations, credibility multipliers, and cluster density. |

---

## 🚀 Quick Start

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Download spaCy model (for NER)
python -m spacy download en_core_web_sm

# 3. Optional: Start Redis & PostgreSQL (for enterprise mode)
# If skipped, VEILORACLE gracefully falls back to SQLite and memory queues.
docker-compose up -d

# 4. Install frontend dependencies
cd frontend && npm install && cd ..

# 5. Run the streaming intelligence pipeline
python main.py pipeline

# 6. Start the API server (port 8000)
# Open a new terminal for this
python main.py server

# 7. Start the frontend (port 5173)
# Open a new terminal for this
python main.py frontend
```

## 📁 Project Structure

```text
VEILORACLE EE Project/
├── backend/
│   ├── queue_manager.py    # Redis/Memory streaming queue layer
│   ├── database.py         # SQLite / PostgreSQL Vector storage layer
│   ├── pipeline.py         # 12-step Async Streaming AI pipeline orchestrator
│   ├── detector.py         # AI: HDBSCAN, Deduplication, Lifecycle, Weighting
│   ├── fake_news.py        # AI: RoBERTa Disinformation detection
│   ├── topic_discovery.py  # AI: BERTopic discovery model
│   ├── multilingual.py     # AI: XLM-RoBERTa translation & mapping
│   ├── sentiment.py        # AI: RoBERTa Sentiment Analysis
│   ├── summarizer.py       # AI: PEGASUS Abstractive Summarization
│   ├── api.py              # FastAPI endpoints 
│   ├── collector.py        # News collection (NewsAPI + RSS + sample data)
│   ├── config.py           # 3000 sectors across ALL global fields
│   ├── predictor.py        # AI: Sector impact prediction
│   ├── preprocessor.py     # AI: NLP text preprocessing
│   ├── ner_engine.py       # AI: spaCy named entity recognition
│   ├── trend_engine.py     # AI: Linear regression trend forecasting
│   └── anomaly_engine.py   # AI: Z-score anomaly detection
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # React app with 6 tabbed AI views
│   │   ├── App.css         # Premium glassmorphism UI styles
│   │   └── index.css       # Base design tokens
│   └── index.html          # SEO-optimized HTML
├── main.py                 # Entry point (pipeline / server / frontend)
├── docker-compose.yml      # Enterprise deployment stack (Postgres + Redis)
├── requirements.txt        # Python dependencies
└── .env.example            # Environment configuration
```

## 🌐 Global Sector Coverage

VEILORACLE monitors **3000+ AI-generated sectors** across every major field:

- 💰 Finance, Banking, Crypto, Insurance, Venture Capital
- 💻 Technology, AI, Cybersecurity, Semiconductors, Cloud
- 🏥 Healthcare, Pharma, Biotech, Mental Health
- ⚡ Energy, Renewables, Oil & Gas, Nuclear
- 🏛️ Politics, Diplomacy, Defense, Law & Justice
- ✈️ Aviation, Shipping, Automotive, Railways
- 🏈 Sports, Olympics, Football, Cricket, Basketball
- 🎬 Entertainment, Film, Music, Gaming, Streaming
- 🔬 Science, Space, Physics, Astronomy
- 🌍 Environment, Climate, Wildlife, Conservation
- 🎓 Education, EdTech, Research, Universities
- 🌾 Agriculture, Food, Fisheries, Organic
- 🏘️ Real Estate, Construction, Housing
- ⚙️ Manufacturing, Robotics, Automation
- 👗 Fashion, Design, Arts, Culture
- ⛏️ Mining, Gold, Lithium, Rare Earth
- ⚖️ Legal, Compliance, Human Rights

## 🖥️ Frontend Features

- **3D Neural Visualization** — Interactive particle sphere (React Three Fiber)
- **AI Intelligence Briefing** — Real-time market mood analysis
- **6 Tabbed Views** — Overview, Sectors, Events, NER Entities, AI Trends, Anomalies
- **Entity Cloud** — AI-extracted people, organizations, locations
- **Trend Forecasting** — Rising/falling sector predictions with confidence scores
- **Anomaly Alerts** — Critical and warning alerts with severity indicators
- **Glassmorphism UI** — Premium dark theme with micro-animations
